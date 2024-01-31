import re
import time
import json
import random
import requests
from lxml import etree
from pytwitter import Api
from selenium import webdriver
from pymysql.converters import escape_string
from TestMethod.db.linkMariaDB import MySqlSSH
from TestMethod.public.HttpU import HttpUtil
proxy = HttpUtil.proxy11   #twitterSearch取代
print('利用Selenium获取twitter分享openai文章')
currentTime = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
bearer_token = "AAAAAAAAAAAAAAAAAAAAALgyqwEAAAAAYcr3gjZVmuDtIL7JSDn0g%2BIG51o%3DZag5vrTtRAhbdw2Z4vsgea18m6P6UdEzbOzGI90jUmMpwIZcFj"
api = Api(proxies=proxy, oauth_flow=True, bearer_token=bearer_token)
# res = api.get_user(username="elonmusk")
postInfo = api.search_tweets(query='chat.openai.com/share',query_type='recent',max_results=100)
# nextId = 'b26v89c19zqg8o3fr5hearm09dk8o7q3gf8j8asec20l9'   ##下页ToKen
# postInfo = api.search_tweets(query='chat.openai.com/share',query_type='recent',next_token=nextId,max_results=100)
newest_id = postInfo.meta.newest_id
next_token = postInfo.meta.next_token
oldest_id = postInfo.meta.oldest_id
print(f'第一页ID为：*--*$-->{next_token}<--$*--*')
num = 0
for initial in postInfo.data:
    num += 1
    twitterId = initial.id
    print(MySqlSSH().querySql('twitterShare', twitterId))
    if MySqlSSH().querySql('twitterShare', twitterId) == '已存在': continue
    repliesText = initial.text
    chatUid = re.findall('https://t.co/([A-Za-z0-9]{10})',str(repliesText),re.S)
    if chatUid:
        chat_dict = []
        twiUrl = []
        for ChatID in chatUid:
            driver = webdriver.Chrome()
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                        Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                        })
                        """
            })
            chatUrl = f'https://t.co/{ChatID}'
            driver.get(chatUrl)
            page_source = driver.page_source
            lxml = etree.HTML(page_source)
            chatInfo = lxml.xpath('//*[@id="__next"]/div[1]/div/main/div[1]/div[1]//text()')
            if chatInfo:
                for dialogue in chatInfo:
                    chat_dict.append(dialogue)
                twiUrl.append(chatUrl)
                driver.quit()
                break
            driver.quit()
        if chat_dict:
            data_dict = dict(
                twitterId=twitterId,
                repliesText=escape_string(str(repliesText)),
                newest_id=newest_id,
                next_token=next_token,
                oldest_id=oldest_id,
                twiUrl=''.join(twiUrl),
                shareTxt=escape_string(str(chat_dict))
            )
            # print(data_dict)
            print(f'正在插入第{num}条')
            MySqlSSH().conn_mysql('twitterShare', data_dict, twitterId)
