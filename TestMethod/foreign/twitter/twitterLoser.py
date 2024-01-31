import time
from pytwitter import Api
from TestMethod.db.linkMariaDB import MySqlSSH
from TestMethod.public.HttpU import HttpUtil
from pymysql.converters import escape_string
class twitterFunction():  #  twitterFull取代  
    def __init__(self,celebrity):
        self.bearer_token = "AAAAAAAAAAAAAAAAAAAAALgyqwEAAAAAYcr3gjZVmuDtIL7JSDn0g%2BIG51o%3DZag5vrTtRAhbdw2Z4vsgea18m6P6UdEzbOzGI90jUmMpwIZc"
        self.api = Api(oauth_flow=True, bearer_token=self.bearer_token)
        self.res = self.api.get_user(username=celebrity)
    def twitterPostsSpider(self):  #  获取最近发布的twitter
        postInfo = self.api.get_timelines(self.res.data.id,exclude=['retweets','replies'],max_results=10)
        newest_id = postInfo.meta.newest_id
        next_token = postInfo.meta.next_token
        oldest_id = postInfo.meta.oldest_id
        print(f'下页ID为：*--*$-->{next_token}<--$*--*')
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
                oldest_id=oldest_id
            )
            print(f'正在插入twitterPosts第{num}条')
            MySqlSSH().conn_mysql('twitterPosts', data_dict, twitterId)
    def twitterRepliesSpider(self):#  获取最近twitter回复 pagination_token=nextId
        info = self.api.get_timelines(self.res.data.id, max_results=50)
        newest_id = info.meta.newest_id
        next_token = info.meta.next_token
        oldest_id = info.meta.oldest_id
        print(f'下页ID为：*--*$-->{next_token}<--$*--*')
        num = 0
        for initial in info.data:
            num += 1
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
                        updateTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    )
                    # print(data_dict)
                    print(f'正在插入twitterReplies第{num}条')
                    MySqlSSH().conn_mysql('twitterReplies', data_dict, twitterId)
            except:
                print("Loser")
if __name__ == '__main__':
    celebrity = 'elonmusk' # twitterName
    twitter = twitterFunction(celebrity)
    # twitter.twitterRepliesSpider()  # 最新回复和原文章
    twitter.twitterPostsSpider()  # 最新发布twitter