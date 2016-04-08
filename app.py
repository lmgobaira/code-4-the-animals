"""
Main application which uses Facebook Graph API (facebook_fetch module) to pass unstructured natural language snippets to IBM Watson
for sentiment analysis. Watson returns a JSON response with aggregate sentiment values. These values are then
checked against a threshold and if meets criteria passed to the slackpost module to be forwarded to Slack.
"""
import json
import time

import numpy as np
import pandas as pd
import slackpost
from facebook_fetch import facebookFetch
from watson_developer_cloud import ToneAnalyzerV3Beta


def gettoneanalysis(content):
    """
    Send plaintext to watson for analysis. Return dict of 5 emotional scores.
    :param content:
    :return:
    """
    #TODO:: Generate new username, and passwords from IBM

    tone_analyzer = ToneAnalyzerV3Beta(username='XXX-1234-XXX-1234',
                                       password='dummy_password',
                                       version='2016-02-11')
    results = json.dumps(tone_analyzer.tone(text=content), indent=2)
    data = json.loads(results)
    contentTones = {}
    for i in data['document_tone']['tone_categories']:
        if i['category_id'] == 'emotion_tone':
            for j in i['tones']:
                contentTones[str(j['tone_name'])] = j['score']
    return contentTones


def checkThresholds(generatedLink, contenttones, contentmessage):
    """
    Run watson results against a threshold based on tone. 1 = 100% of category.
    :param contentmessage:
    :param contenttones:
    :param generatedLink:
    """

    angerThreshold = .5
    joyThreshold = .3
    fearThreshold = .5
    sadThreshold = .5
    disgustThreshold = .5

    if contenttones['Joy'] < joyThreshold:

        if contenttones['Disgust'] > disgustThreshold:
            slackpost.pushToSlack(link=generatedLink, channel='C0QKRPA1G', message=contentmessage)

        if contenttones['Anger'] > angerThreshold:
            slackpost.pushToSlack(link=generatedLink, channel='C0QKRPA1G', message=contentmessage)

        if contenttones['Fear'] > fearThreshold:
            slackpost.pushToSlack(link=generatedLink, channel='C0QKRPA1G', message=contentmessage)

        if contenttones['Sadness'] > sadThreshold:
            slackpost.pushToSlack(link=generatedLink, channel='C0QKRPA1G', message=contentmessage)


def stamp_time_now():
    """
    Store the current epoch time for later
    """

    int_time_now = int(time.time())
    f = open('last_run', 'r+')
    text = str(int_time_now)
    f.seek(0)
    f.write(text)
    f.truncate()
    f.close()

def last_run_time():
    """
    Returns the last script run time
    """
    f = open('last_run', 'r+')
    f.seek(0)
    t = f.read()
    f.close()
    if ((t is None) or (t == '')):
        t = int(time.time())
    return int(t)


def analyze():
    """
    Main program entry point.
    Fetches data from Facebook Open Graph API
    Submits to Watson for analysis
    Generate Facebook Link
    Checks Thresholds and Post to Slack
    :return:
    """
    df = facebookFetch()

    # Transform the ISO date to Epoch
    df['epoch_int'] = pd.DatetimeIndex(df['created_time']).astype(np.int64)
    df['epoch_int'] /= 10 ** 9

    # Drop rows in the DataFrame where the created_time < last_run_time
    df = df[df.epoch_int > last_run_time()]

    for index, row in df.iterrows():
        if len(str(row['message'])) != 0:
            print('Sending Row to Watson for Review:', (row['id']))
            tone = gettoneanalysis(content=row['message'])
            idcode = row['id'].split("_")

            if str(row['accountID']) == 'nan':
                generatedlink = "https://www.facebook.com/" + idcode[0]
            else:
                generatedlink = "https://www.facebook.com/" + idcode[0] + "/posts/" + idcode[1]

            checkThresholds(generatedLink=generatedlink, contenttones=tone, contentmessage=row['message'][:140])
        else:
            print('Skipping Row..')
    return 0

if __name__ == '__main__':
    analyze()
    stamp_time_now()

