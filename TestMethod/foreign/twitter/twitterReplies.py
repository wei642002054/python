import random
import time
import requests
from pymysql.converters import escape_string
from pytwitter import Api
from TestMethod.db.linkMariaDB import MySqlSSH
from TestMethod.public.HttpU import HttpUtil
proxy = HttpUtil.proxy11
bearer_token = "AAAAAAAAAAAAAAAAAAAAALgyqwEAAAAAYcr3gjZVmuDtIL7JSDn0g%2BIG51o%3DZag5vrTtRAhbdw2Z4vsgea18m6P6UdEzbOzGI90jUmMpwIZcFj"
api = Api(proxies=proxy, oauth_flow=True, bearer_token=bearer_token)
res = api.get_user(username="elonmusk")
def initialSpider():
    # xx = api.get_users(ids=["783214", "2244994945"])
    nextTokne = '7140dibdnow9c7btw481cuhl3xkwl04bahahas17l0ncj'
    info = api.get_timelines(res.data.id,pagination_token=nextTokne, max_results=100)
    # info = api.get_timelines(res.data.id,max_results=100)
    newest_id = info.meta.newest_id
    next_token = info.meta.next_token
    oldest_id = info.meta.oldest_id
    print(f'下一页ID为：*--*$-->{next_token}<--$*--*')
    num = 0
    for initial in info.data:
        num +=1
        twitterId = initial.id
        print(MySqlSSH().querySql('twitterReplies',twitterId))
        if MySqlSSH().querySql('twitterReplies',twitterId) == '已存在':continue
        url = f'https://api.twitter.com/2/tweets?ids={twitterId}&tweet.fields=author_id,conversation_id,created_at,in_reply_to_user_id,' \
              f'referenced_tweets&expansions=author_id,in_reply_to_user_id,referenced_tweets.id&user.fields=name,username'
        bearer_token = "AAAAAAAAAAAAAAAAAAAAALgyqwEAAAAAYcr3gjZVmuDtIL7JSD" \
                       "n0g%2BIG51o%3DZag5vrTtRAhbdw2Z4vsgea18m6P6UdEzbOzGI90jUmMpwIZcFj"
        header ={'Authorization':'Bearer {}'.format(bearer_token)}
        try:
            resp = HttpUtil().gain(url,header)
            result = resp.json().get('includes').get('tweets')
            if result:
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
                    twitterName='elonmusk',
                    updateTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                )
                print(f'正在插入第{num}条')
                MySqlSSH().conn_mysql('twitterReplies', data_dict, twitterId)
        except:
            print("Loser")
    # nextSpider(newest_id)
def nextSpider(nextId):
    try:   #有问题  得优化程序
        nextInfo = api.get_timelines(res.data.id,pagination_token=nextId,max_results=100)
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
            MySqlSSH().conn_mysql('twitterReplies', data_dict, twitterId)
        nextSpider(nextInfo.meta.next_token)
    except:
        print('访问受限等待15分钟重新获取')
        time.sleep(900)  #获取最后一条数据的Next页
        nextToken = MySqlSSH().getFinally('twitterReplies', 'createTime')
        if nextToken != 'None':
            nextSpider(nextToken)
        return
if __name__ == '__main__':
    initialSpider()