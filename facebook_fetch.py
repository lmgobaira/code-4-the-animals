"""
This modules generates a FB access token, grabs posts and comments then creates a pandas dataframe with scraped content.
"""
import pandas as pd
import requests

#TODO :: Genereate new client id and client secret from Facebook "https://developers.facebook.com/"

# Define Facebook credentials
fb_client_id = 'XXXXXXX'
fb_client_secret = 'XXXXXXXXXX'
req = requests.get('https://graph.facebook.com/oauth/access_token?client_id={}&client_secret={}&grant_type=client_credentials'.format(
        fb_client_id,fb_client_secret))
access_token = req.text


#TODO:: Update list to include accounts you would like to check.
accounts = ['TheHiddenTruthBehindTheBars',
            '586954868007471',
            'urgentdogsofmiami',
            'mdasadopt']


def getChildrenFromObject(objectID):
    """

    :param objectID:
    :return:
    """
    child_req = requests.get('https://graph.facebook.com/'+objectID+'/comments/?filter=stream&'+access_token)
    child_req_json = child_req.json()
    child_data = child_req_json['data']
    df = pd.DataFrame(child_data)
    return df


def getParentsFromAccount(accountID):
    """

    :param accountID:
    :return:
    """
    parent_req = requests.get('https://graph.facebook.com/'+accountID+'/feed?'+access_token)
    parent_req_json = parent_req.json()
    parent_data = parent_req_json['data']
    df = pd.DataFrame(parent_data)
    df['accountID'] = accountID
    return df


def facebookFetch():
    """
    Main pandas logic to create list of posts, and comments to feed back to calling function.

    :return:
    """

    parents_df = pd.DataFrame()
    children_df = pd.DataFrame()

    # Construct a DataFrame for the parent posts
    for account in accounts:
        df = getParentsFromAccount(account)
        parents_df = parents_df.append(df)

    # Construct a DataFrame for the childrens posts
    for index, row in parents_df.iterrows():
        df = getChildrenFromObject(row['id'])
        children_df = children_df.append(df)

    # Group common fields for Watson
    parents_df_cols = ['created_time', 'message', 'id', 'accountID']
    parents_df = parents_df[parents_df_cols]

    children_df_cols = ['created_time', 'message', 'id']
    children_df = children_df[children_df_cols]

    combined_df = pd.concat((parents_df, children_df))

    combined_df.dropna(subset=['message'], inplace=True)

    combined_df['created_time'] = pd.to_datetime(combined_df['created_time'])

    return combined_df

