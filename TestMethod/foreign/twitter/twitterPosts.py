import time
from fake_useragent import UserAgent
import requests,random
# from curl_cffi import requests
from pymysql.converters import escape_string
from pytwitter import Api
from TestMethod.db.linkMariaDB import MySqlSSH
from TestMethod.public.HttpU import HttpUtil
import tweepy
from TwitterAPI import TwitterAPI, TwitterPager
proxy = HttpUtil.proxy11
bearer_token = "AAAAAAAAAAAAAAAAAAAAALgyqwEAAAAAYcr3gjZVmuDtIL7JSDn0g%2BIG51o%3DZag5vrTtRAhbdw2Z4vsgea18m6P6UdEzbOzGI90jUmMpwIZcFj"
api = Api(proxies=proxy, oauth_flow=True, bearer_token=bearer_token)
res = api.get_user(username="elonmusk")
def firstSpider():
    postInfo = api.get_timelines(res.data.id,exclude=['retweets','replies'],max_results=10)
    newest_id = postInfo.meta.newest_id
    next_token = postInfo.meta.next_token
    oldest_id = postInfo.meta.oldest_id
    print(f'第一页ID为：*--*$-->{next_token}<--$*--*')
    num = 0
    for initial in postInfo.data:
        num +=1
        twitterId = initial.id
        repliesText = initial.text
        data_dict = dict(
            twitterId=twitterId,
            repliesText=escape_string(str(repliesText)),
            newest_id=newest_id,
            next_token=next_token,
            oldest_id=oldest_id,
            twitterName='elonmusk'
        )
        print(f'正在插入第{num}条')
        MySqlSSH().conn_mysql('twitterPosts', data_dict, twitterId)
    # nextSpider(newest_id)
def nextSpider(nextId):
    try:
        time.sleep(3)
        nextInfo = api.get_timelines(res.data.id,pagination_token=nextId,exclude=['retweets','replies'],max_results=100)
        print(f'下一页ID为：*--*$-->{nextInfo.meta.next_token}<--$*--*')
        newest_id = nextInfo.meta.newest_id
        next_token = nextInfo.meta.next_token
        oldest_id = nextInfo.meta.oldest_id
        num = 0
        for i in nextInfo.data:
            num +=1
            twitterId = i.id
            repliesText = i.text
            data_dict = dict(
                twitterId=twitterId,
                repliesText=escape_string(str(repliesText)),
                newest_id=newest_id,
                next_token=next_token,
                oldest_id=oldest_id,
                twitterName='elonmusk'
            )
            print(f'正在插入第{num}条')
            MySqlSSH().conn_mysql('twitterPosts', data_dict, twitterId)
        nextSpider(nextInfo.meta.next_token)
    except:
        print('访问受限等待15分钟重新获取')
        time.sleep(900)  #获取最后一条数据的Next页
        nextToken = MySqlSSH().getFinally('twitterPosts', 'createTime')
        if nextToken != 'None':
            nextSpider(nextToken)
        return
firstSpider()














# bearer_token = "AAAAAAAAAAAAAAAAAAAAALgyqwEAAAAAYcr3gjZVmuDtIL7JSDn0g%2BIG51o%3DZag5vrTtRAhbdw2Z4vsgea18m6P6UdEzbOzGI90jUmMpwIZcFj"
# api = Api(proxies=proxy, oauth_flow=True, bearer_token=bearer_token)
# res = api.get_user(username="elonmusk")
# # url = 'https://api.twitter.com/2/tweets/44196397/quote_tweets'
# info = api.get_timelines(res.data.id,max_results=10)
# print(info)
# #
