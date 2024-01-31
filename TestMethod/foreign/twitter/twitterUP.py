import time,requests
import pymysql,random
from pymysql.converters import escape_string
from pytwitter import Api
from sshtunnel import SSHTunnelForwarder
from TestMethod.db.linkMariaDB import MySqlSSH
from TestMethod.public.HttpU import HttpUtil
proxy = HttpUtil.proxy11
def searchSql(databash):
    server = SSHTunnelForwarder(
        ssh_address_or_host=('aliyun-bj1.tongyuan.ai', 22),
        ssh_username='root',
        ssh_password='3HpvNIfT8WNZnAc4',
        remote_bind_address=('127.0.0.1', 3307)
    )
    # 启动隧道服务
    server.start()
    mysql_config = {
        'user': 'root',
        'passwd': 'my-secret-pw',
        'host': '127.0.0.1',
        'port': server.local_bind_port,
        'db': 'SpiderData',
    }
    # 连接数据库
    db = pymysql.connect(**mysql_config)
    cursor = db.cursor()
    mysql = f'select twitterId from {databash} '
    cursor.execute(mysql)
    info = cursor.fetchall()
    return info
def upSpider(databash):
    num = 0
    for i in searchSql(databash):
        num +=1
        # if num < 2478:
        #     continue
        url = f'https://api.twitter.com/2/tweets?ids={i[0]}&tweet.fields=author_id,conversation_id,created_at,in_reply_to_user_id,' \
              f'referenced_tweets&expansions=author_id,in_reply_to_user_id,referenced_tweets.id&user.fields=name,username'
        bearer_token = "AAAAAAAAAAAAAAAAAAAAALgyqwEAAAAAYcr3gjZVmuDtIL7JSD" \
                       "n0g%2BIG51o%3DZag5vrTtRAhbdw2Z4vsgea18m6P6UdEzbOzGI90jUmMpwIZcFj"
        header ={'Authorization':'Bearer {}'.format(bearer_token)}
        print(f'正在更新第{num}条--->{i[0]}')
        resp = HttpUtil().gain(url,header)  #获取详情帖子
        result = resp.json().get('includes').get('tweets')
        if result:
            source_text = result[0].get('text')
            source_id = result[0].get('id')
            author_id = result[0].get('author_id')
            data_dict = dict(
                source_text = escape_string(str(source_text)),
                source_id = source_id,
                author_id = author_id,
            )
            MySqlSSH().updata(databash,data_dict,i[0])
upSpider('twitterReplies')




