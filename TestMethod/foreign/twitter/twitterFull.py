import time,json
import urllib.request
from pytwitter import Api
from urllib.error import HTTPError
from TestMethod.public.HttpU import HttpUtil
from pymysql.converters import escape_string
from TestMethod.db.linkMariaDB import MySqlSSH
proxy = HttpUtil.proxy11
class twitterFunction():
    def __init__(self,celebrity):
        self.bearer_token = "AAAAAAAAAAAAAAAAAAAAALgyqwEAAAAAYcr3gjZVmuDtIL7JSDn0g%2BIG51o%3DZag5vrTtRAhbdw2Z4vsgea18m6P6UdEzbOzGI90jUmMpwIZcFj"
        self.api = Api(proxies=proxy, oauth_flow=True, bearer_token=self.bearer_token)
        self.res = self.api.get_user(username=celebrity)
        ## -------------------------------------------- ##
        self.TWITTER_USERNAME = celebrity
        self.headers = {
            'Authorization': 'Bearer ' + self.bearer_token  # os.environ['BEARER_TOKEN']
        }
        self.SAVE_FILENAME = self.TWITTER_USERNAME + "-tweets.json"
        self.DEBUG = False

        self.all_tweets = {
            "meta": {
                "result_count": 0,
                "next_token": None
            },
            "data": []
        }
        try:
            with open(self.SAVE_FILENAME, 'r') as f:
                self.all_tweets = json.loads(f.read())
                print('Loaded saved progress with ' + str(self.all_tweets["meta"]["result_count"]) + ' tweets')
        except:
            print('Saved progress file not found, start fresh...')

        self.tweet_fields = "edit_history_tweet_ids,attachments,author_id,conversation_id,created_at,edit_controls,entities,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,withheld"
        self.all_api_base = "https://api.twitter.com/2/tweets/search/all"
        self.all_params = {
            "query": "from:" + self.TWITTER_USERNAME,
            "tweet.fields": self.tweet_fields,
            "max_results": 50,
            # although it allows max 500 requests, but we cannot fetch 500 related tweets at once since the URL would be too long
            "start_time": "2006-04-01T00:00:00.00Z",  # if the date is too early (e.g. 2000-01-01), it would return 400
        }

        self.tweets_api_base = "https://api.twitter.com/2/tweets"
        self.tweets_params = {
            "ids": 0,
            "tweet.fields": self.tweet_fields
        }
    def twitterPostsSpider(self):  #  获取最近发布的twitter
        startTime = time.time()
        postInfo = self.api.get_timelines(self.res.data.id,exclude=['retweets','replies'],max_results=10)
        newest_id = postInfo.meta.newest_id
        next_token = postInfo.meta.next_token
        oldest_id = postInfo.meta.oldest_id
        print(f'下页ID为：*--*$-->{ next_token}<--$*--*')
        num = 0
        postsJson = []
        for initial in postInfo.data:
            twitterId = initial.id
            if MySqlSSH().querySql('twitterPosts', twitterId) == '已存在': continue
            num +=1
            repliesText = initial.text
            data_dict = dict(
                twitterId=twitterId,
                repliesText=escape_string(str(repliesText)),
                newest_id=newest_id,
                next_token=next_token,
                oldest_id=oldest_id,
                twitterName=self.TWITTER_USERNAME,
            )
            postsJson.append(data_dict)
            print(f'正在插入twitterPosts第{num}条')
            MySqlSSH().conn_mysql('twitterPosts', data_dict, twitterId)
        endTime = time.time()
        # json_str = json.dumps(postsJson, ensure_ascii=False, indent=2)
        infoTime = round(endTime-startTime,2)
        if postsJson==[]:postsJson='无新发布信息'
        returned_data = {
            'twitterName': self.TWITTER_USERNAME,
            'wasteTime': str(infoTime)+'秒',
            'number':num,
            'data': postsJson}
        # print(returned_data)
        return returned_data
        # print(f'耗时{infoTime}秒完成',num,postsJson)
    def twitterRepliesSpider(self):#  获取最近twitter回复 pagination_token=nextId
        startTime = time.time()
        info = self.api.get_timelines(self.res.data.id, max_results=30)
        newest_id = info.meta.newest_id
        next_token = info.meta.next_token
        oldest_id = info.meta.oldest_id
        print(f'下页ID为：*--*$-->{next_token}<--$*--*')
        num = 0
        repliesJson = []
        for initial in info.data:
            twitterId = initial.id
            print(MySqlSSH().querySql('twitterReplies', twitterId))
            if MySqlSSH().querySql('twitterReplies', twitterId) == '已存在': continue
            url = f'https://api.twitter.com/2/tweets?ids={twitterId}&tweet.fields=author_id,conversation_id,created_at,in_reply_to_user_id,' \
                  f'referenced_tweets&expansions=author_id,in_reply_to_user_id,referenced_tweets.id&user.fields=name,username'
            header = {'Authorization': 'Bearer {}'.format(self.bearer_token)}
            try:
                resp = HttpUtil().gain(url, header)
                result = resp.json().get('includes').get('tweets')
                if result:
                    num += 1
                    source_text = result[0].get('text')
                    source_id = result[0].get('id')
                    author_id = result[0].get('author_id')
                    repliesText = initial.text
                    data_dict = dict(
                        twitterId=twitterId,
                        repliesText=escape_string(str(repliesText)),
                        newest_id=newest_id,
                        next_token=next_token,
                        oldest_id=oldest_id,
                        source_text=escape_string(str(source_text)),
                        source_id=source_id,
                        author_id=author_id,
                        twitterName=self.TWITTER_USERNAME,
                        updateTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    )
                    # print(data_dict)
                    repliesJson.append(data_dict)
                    print(f'正在插入twitterReplies第{num}条')
                    MySqlSSH().conn_mysql('twitterReplies', data_dict, twitterId)
            except:
                print("Loser")
        endTime = time.time()
        infoTime = round(endTime-startTime,2)
        if repliesJson==[]:repliesJson='无新发布信息'
        returned_data = {
            'twitterName': self.TWITTER_USERNAME,
            'wasteTime': str(infoTime)+'秒',
            'number':num,
            'data': repliesJson}
        print(returned_data)
        # print(f'耗时{infoTime}秒完成',num,repliesJson)
    def get_json(self,url_base, params):
        url = url_base
        if len(params) > 0:
            url += '?' + '&'.join([k + '=' + str(params[k]) for k in params])
        req = urllib.request.Request(url, headers=self.headers)
        while True:
            try:
                response = urllib.request.urlopen(req)
            except HTTPError as http_error:
                if http_error.status == 429:
                    print('Twitter API 429 Error, waiting and retry...')
                    time.sleep(1)
                    continue
                else:
                    raise http_error
            break
        string_response = response.read().decode('utf-8')
        return json.loads(string_response)
    def runHistorySpider(self):
        while True:
            if self.all_tweets['meta']['next_token']:
                self.all_params['next_token'] = self.all_tweets['meta']['next_token']
            json_response = self.get_json(self.all_api_base, self.all_params)

            all_referenced_ids = []
            if "data" not in json_response:
                print('No results found')
                break
            for tweet in json_response["data"]:
                if 'referenced_tweets' in tweet:
                    for ref in tweet['referenced_tweets']:
                        all_referenced_ids.append(str(ref['id']))
            self.tweets_params['ids'] = ','.join(all_referenced_ids)
            ref_tweet_json = self.get_json(self.tweets_api_base, self.tweets_params)
            ref_tweets_by_id = {}
            if 'data' in ref_tweet_json:
                for ref_tweet in ref_tweet_json['data']:
                    ref_tweets_by_id[ref_tweet['id']] = ref_tweet

            last_created_at = None
            for tweet in json_response["data"]:
                if self.DEBUG:
                    print(tweet['created_at'], tweet['text'])
                if 'referenced_tweets' in tweet:
                    for idx in range(len(tweet['referenced_tweets'])):
                        ref_id = tweet['referenced_tweets'][idx]['id']
                        if ref_id in ref_tweets_by_id:
                            tweet['referenced_tweets'][idx]['data'] = ref_tweets_by_id[ref_id]
                            if self.DEBUG:
                                print('Referenced tweet:', ref_tweets_by_id[ref_id]['created_at'],
                                      ref_tweets_by_id[ref_id]['text'])
                        else:
                            print('Reference tweet ID', ref_id, 'not found')
                self.all_tweets['data'].append(tweet)
                last_created_at = tweet['created_at']

            self.all_tweets['meta']['result_count'] += json_response['meta']['result_count']
            self.all_tweets['meta']['next_token'] = json_response['meta']['next_token'] if 'next_token' in json_response[
                'meta'] else None
            with open(self.SAVE_FILENAME, 'w') as f:
                f.write(json.dumps(self.all_tweets))
            print('Saved', self.all_tweets['meta']['result_count'], last_created_at)
            if self.all_tweets['meta']['next_token'] is None:
                break
if __name__ == '__main__':
    celebrity = 'elonmusk' # #BillMelugin_ Jason   elonmusk
    twitter = twitterFunction(celebrity)
    twitter.twitterRepliesSpider()  # 最新回复和原文章
    # twitter.twitterPostsSpider()  # 最新发布twitter
    # twitter.runHistorySpider()   #获取06-23历史数据
