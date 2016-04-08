"""
This module uses requests library to HTTP POST message to slack.
1 - Generate a token via https://api.slack.com/tokens
2 - Find channel Ids via https://api.slack.com/methods/channels.list/test

"""

import requests


#TODO:: Insert your unique Slack auth token here.
token = 'xxxxx-1234-xxxx-4567'
method = 'chat.postMessage'

def pushToSlack(link, channel='XXXXXXX', message='DEFAULT'):
    """
    :param message:
    :param channel:
    :param link:
    :link:      *Required*  The link to the negative post

    :channel:   *Optional*  The channel to post via an ID. The channels below are unique to each slack instance.
                  general = XXXXXXXX
                  negative = XXXXXXX (default)
                  positive = XXXXXXX
                  all-posts = XXXXXX

    :text:      *Optional* What text to post to slack, there is a pretty
                default if this is empty.
    """

    if link is None:
        # No link was passed, can't continue
        raise Exception('You need to give me a link to send.')
    else:
        # A link was passed correctly, continue
        if message == 'DEFAULT':
            text = """Something was posted to Facebook that looks to be negative.
            \nRead it here: {}""".format(link) + "\n *****"
        else:
            text = """Something was posted to Facebook that looks to be negative.
            \nRead it here: {}""".format(link) + "\n" + message + "\n *****"
        # Continue to post to Slack
        requests.post('https://slack.com/api/{}?token={}&channel={}&text={}'.format(
            method,
            token,
            channel,
            text
            ))

        return 0
