import random
import re
import time
import requests
from lxml import etree

from TestMethod.public.HttpU import HttpUtil
proxy = HttpUtil.proxy11
user_agent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    'Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.9.2.1000 Chrome/39.0.2146.0 Safari/537.36',
    'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/532.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/532.3',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'
]
headers = {
    "User-Agent": random.choice(user_agent),
}
url = 'https://wiki.biligame.com/ys/%E5%9D%8E%E8%92%82%E4%B8%9D%E8%AF%AD%E9%9F%B3'
# url = 'https://wiki.biligame.com/ys/%E7%BA%B3%E8%A5%BF%E5%A6%B2%E8%AF%AD%E9%9F%B3'
# url = 'https://mbd.baidu.com/newspage/data/landingshare?context=%7B%22nid%22%3A%22news_9685184585648334730%22%2C%22sourceFrom%22%3A%22wise_feedlist%22%7D&rec_src=52'
resp = requests.get(url = url,headers=headers)
lxml = etree.HTML(resp.text)
all = lxml.xpath('//div[@class="resp-tabs-container"]/div[1]//table[@class="wikitable"]/tbody')
num = 0
for i in all:
    num +=1
    introduce = ''.join(i.xpath('./tr[1]/th/text()')).strip()
    china = ''.join(i.xpath('./tr[4]/td/div[1]/text()')).strip()
    Japanese = ''.join(i.xpath('./tr[4]/td/div[2]/text()')).strip()
    English = ''.join(i.xpath('./tr[4]/td/div[3]/text()')).strip()
    Korean = ''.join(i.xpath('./tr[4]/td/div[4]/text()')).strip()
    chinaAudio = ''.join(i.xpath('./tr[3]/td[1]/div/@data-src')).strip()
    print(chinaAudio,type(chinaAudio))
    if chinaAudio:
        ChFile = ''.join(re.findall('\.com/.*/(.*)', chinaAudio, re.S)).strip()
    JapanAudio = ''.join(i.xpath('./tr[3]/td[2]/div/@data-src')).strip()
    JPNFile = ''.join(re.findall('\.com/.*/(.*)', JapanAudio, re.S)).strip()
    EngliAudio = ''.join(i.xpath('./tr[3]/td[3]/div/@data-src')).strip()
    EnFile = ''.join(re.findall('\.com/.*/(.*)', EngliAudio, re.S)).strip()
    KoreanAudio = ''.join(i.xpath('./tr[3]/td[4]/div/@data-src')).strip()
    KrFile = ''.join(re.findall('\.com/.*/(.*)', KoreanAudio, re.S)).strip()
    print(introduce,china)