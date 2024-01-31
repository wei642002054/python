import urllib.request
from urllib.error import HTTPError
import json
import os
import time
import sys

TWITTER_USERNAME = sys.argv[1]
SAVE_FILENAME = TWITTER_USERNAME + "-tweets.json"
DEBUG = False

all_tweets = {
    "meta": {
        "result_count": 0,
        "next_token": None
    },
    "data": []
}
try:
    with open(SAVE_FILENAME, 'r') as f:
        all_tweets = json.loads(f.read())
        print('Loaded saved progress with ' + str(all_tweets["meta"]["result_count"]) + ' tweets')
except:
    print('Saved progress file not found, start fresh...')

tweet_fields = "edit_history_tweet_ids,attachments,author_id,conversation_id,created_at,edit_controls,entities,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,withheld"
all_api_base = "https://api.twitter.com/2/tweets/search/all"
all_params = {
    "query": "from:" + TWITTER_USERNAME,
    "tweet.fields": tweet_fields,
    "max_results": 50,   # although it allows max 500 requests, but we cannot fetch 500 related tweets at once since the URL would be too long
    "start_time": "2006-04-01T00:00:00.00Z",  # if the date is too early (e.g. 2000-01-01), it would return 400
}

tweets_api_base = "https://api.twitter.com/2/tweets"
tweets_params = {
    "ids": 0,
    "tweet.fields": tweet_fields
}

headers = {
    'Authorization': 'Bearer ' + os.environ['BEARER_TOKEN']
}

def get_json(url_base, params):
    url = url_base
    if len(params) > 0:
        url += '?' + '&'.join([ k + '=' + str(params[k]) for k in params ])
    req = urllib.request.Request(url, headers=headers)
    while True:
        try:
            response = urllib.request.urlopen(req)
        except HTTPError as http_error:
            if http_error.status == 429:
                print('Twitter API 429 Error, waiting and retry...')
                time.sleep(1)
                continue
            elif http_error.status == 503:
                print('Twitter API 503 Error, waiting and retry...')
                time.sleep(1)
                continue
            else:
                print(url)
                raise http_error
        break
    string_response = response.read().decode('utf-8')
    return json.loads(string_response)


while True:
    if all_tweets['meta']['next_token']:
        all_params['next_token'] = all_tweets['meta']['next_token']
    json_response = get_json(all_api_base, all_params)

    all_referenced_ids = []
    if "data" not in json_response:
        print('No results found')
        break
    for tweet in json_response["data"]:
        if 'referenced_tweets' in tweet:
            for ref in tweet['referenced_tweets']:
                all_referenced_ids.append(str(ref['id']))

    ref_tweets_by_id = {}
    if len(all_referenced_ids) > 0:
        tweets_params['ids'] = ','.join(all_referenced_ids)
        ref_tweet_json = get_json(tweets_api_base, tweets_params)
        if 'data' in ref_tweet_json:
            for ref_tweet in ref_tweet_json['data']:
                ref_tweets_by_id[ref_tweet['id']] = ref_tweet

    last_created_at = None
    for tweet in json_response["data"]:
        if DEBUG:
            print(tweet['created_at'], tweet['text'])
        if 'referenced_tweets' in tweet:
            for idx in range(len(tweet['referenced_tweets'])):
                ref_id = tweet['referenced_tweets'][idx]['id']
                if ref_id in ref_tweets_by_id:
                    tweet['referenced_tweets'][idx]['data'] = ref_tweets_by_id[ref_id]
                    if DEBUG:
                        print('Referenced tweet:', ref_tweets_by_id[ref_id]['created_at'], ref_tweets_by_id[ref_id]['text'])
                else:
                    print('Reference tweet ID', ref_id, 'not found')
        all_tweets['data'].append(tweet)
        last_created_at = tweet['created_at']

    all_tweets['meta']['result_count'] += json_response['meta']['result_count']
    all_tweets['meta']['next_token'] = json_response['meta']['next_token'] if 'next_token' in json_response['meta'] else None
    with open(SAVE_FILENAME, 'w') as f:
        f.write(json.dumps(all_tweets))
    print('Saved', all_tweets['meta']['result_count'], last_created_at)

    if all_tweets['meta']['next_token'] is None:
        break
