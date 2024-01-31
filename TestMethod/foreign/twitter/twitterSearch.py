import openai,time
import json,re
from orjson import dumps
import httpx
import random
import requests
import warnings
import urllib3
from pytwitter import Api
from pymysql.converters import escape_string
from TestMethod.db.linkMariaDB import MySqlSSH
from TestMethod.public.HttpU import HttpUtil
from curl_cffi import requests
proxy = HttpUtil.proxy11
class TwitSearch():  #获取twitter分享openai文章
    def __init__(self):
        self.TLSAll = ["edge99", "edge101", "chrome99", "chrome100", "chrome101", "chrome104", "chrome107", "chrome110",
                  "chrome99_android", "safari15_3", "safari15_5"]
        self.TLS = random.choice(self.TLSAll)
        self.currentTime = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
        bearer_token = "AAAAAAAAAAAAAAAAAAAAALgyqwEAAAAAYcr3gjZVmuDtIL7JSDn0g%2BIG51o%3DZag5vrTtRAhbdw2Z4vsgea18m6P6UdEzbOzGI90jUmMpwIZcFj"
        self.api = Api(proxies=proxy, oauth_flow=True, bearer_token=bearer_token)
        self.headers = {
            'Content-Type': 'application/json',
            'Host':'chat.openai.com',
            'Referer':'https://t.co/',
            'Authorization': 'Bearer {}'.format(bearer_token),
            'Sec-Ch-Ua':'"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
    def redirectSpider(self,nextToken):
        import requests  #
        # postInfo = self.api.search_tweets(query='chat.openai.com/share', query_type='recent', max_results=100)
        # nextToken ='b26v89c19zqg8o3fr5hfjrfiy3g5wgaokvcm2dyay5oxp' ##下页 ToKen
        postInfo = self.api.search_tweets(query='chat.openai.com/share',query_type='recent',next_token=nextToken,max_results=10)
        newest_id = postInfo.meta.newest_id
        next_token = postInfo.meta.next_token
        oldest_id = postInfo.meta.oldest_id
        print(f'下页ID为：*--*$-->{next_token}<--$*--*')
        num = 1
        for initial in postInfo.data:
            twitterId = initial.id
            print(MySqlSSH().querySql('twitterShare', twitterId))
            if MySqlSSH().querySql('twitterShare', twitterId) == '已存在': continue
            repliesText = initial.text
            chatUid = re.findall('https://t.co/([A-Za-z0-9]{10})', str(repliesText), re.S)
            if chatUid:
                for ChatID in chatUid:
                    chatUrl = f'https://t.co/{ChatID}'
                    # url = 'https://t.co/gH6ZwS3gpK'
                    response = requests.head(url=chatUrl,proxies=proxy)
                    # 获取响应头信息
                    headers = response.headers
                    print(f'{twitterId}--正在获取{num}条--->{chatUrl}')
                    if 'chat.openai' not in headers.get('location'):
                        continue
                    num +=1
                    openAiUrl = headers.get('location')
                    redirect_data = dict(
                        twitterId=twitterId,
                        repliesText=escape_string(str(repliesText)),
                        newest_id=newest_id,
                        next_token=next_token,
                        oldest_id=oldest_id,
                        twiUrl=''.join(chatUrl)
                    )
                    self.resultSpider(redirect_data=redirect_data,openAiUrl=openAiUrl)
    def resultSpider(self,**kwargs):
        # 发送HEAD请求
        data = kwargs.get('redirect_data')
        twitterId = data.get('twitterId')
        url = kwargs.get('openAiUrl')
        resp = HttpUtil().Rget(url,self.headers)
        # url = "https://chat.openai.com/share/1f907c91-923b-43ec-b97c-ac1785aa8be3"
        # resp = requests.get(url=url,headers=self.headers,impersonate=self.TLS,proxies=proxy,verify=False)
        try:
            info = ''.join(re.findall('serverResponse.*?"data":(.*?)},.continueMode',str(resp.text),re.S)).strip()
            data_dict=dict(
                shareTxt=escape_string(str(info)),
                updateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            )
            data.update(data_dict)
            MySqlSSH().conn_mysql('twitterShare', data, twitterId)
        except:
            print('URL——>LOSET')
if __name__ == '__main__':
    spider = TwitSearch()
    number = 0
    while True:
        number+=1
        if number >=2:  #11
            break   #获取最后一个Token
        nextToken = MySqlSSH().getFinally('twitterShare', 'createTime')
        print(nextToken)
        if nextToken != 'None':
            spider.redirectSpider(nextToken)
