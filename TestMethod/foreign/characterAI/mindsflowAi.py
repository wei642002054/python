import re,json
from lxml import etree
from pymysql.converters import escape_string
import requests
import time,random
from newspaper import Article
from TestMethod.db.linkMariaDB import MySqlSSH  #httpMethod
from TestMethod.public.HttpU import HttpUtil
from TestMethod.foreign.characterAI.mindsDict import replaceDict
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
    "User-Agent": random.choice(user_agent)
}
proxy = HttpUtil.proxy11
def downloadImgSpider(img_url): # 下载图片
    ImgFileId = ''.join(re.findall('\.net/(.*?)/', str(img_url), re.S)).strip()
    response = requests.get(url=img_url, headers=headers, proxies=proxy, verify=False, timeout=18)
    with open(r"E:\Img\mindsflowImg/{}".format(ImgFileId) + '.webp', "wb") as f:  # 下载封面
        f.write(response.content)
def infoSpider(page,categoryId,tag):
    url = f'https://api.mindsflow.ai/history/developer/agents/by-category?pageSize=24&pageNumber={page}&categoryId={categoryId}'
    resp = requests.get(url=url,headers=headers,proxies=proxy,timeout=8,verify=False)
    result = resp.json().get('content')
    totalPages = resp.json().get('pagination').get('totalPages')
    print(f'正在获取{tag}-{page}页',totalPages,url)
    if result:
        for i in result:
            data_dict = dict(
            name = escape_string(str(replaceDict(i.get('name')))),
            tags = tag,
            tagsId = categoryId,
            screenName = i.get('screenName'),
            category = escape_string(str(i.get('category'))),
            greeting = escape_string(str(replaceDict(i.get('greeting')))),  #替换内容
            prompt = escape_string(str(replaceDict(i.get('prompt')))),  #替换内容
            description = escape_string(str(replaceDict(i.get('description')))),  #替换内容
            model = i.get('model'),
            avatar = i.get('avatar'),
            totalFork = i.get('totalFork'),
            totalChat = i.get('totalChat'),
            status = i.get('status'),
            createdAt = i.get('createdAt'),
            updatedAt = i.get('updatedAt'),
            user = escape_string(str(i.get('user')))
            )
            img_url = i.get('avatar')
            if img_url:downloadImgSpider(img_url)
            # print(data_dict)
            MySqlSSH().fetch_all('mindsflowAi', data_dict, 'avatar', img_url)
        if totalPages > 1:
            page += 1
            if page >= totalPages:return 'False'
            infoSpider(page,categoryId,tag)
        return 'False'
if __name__ == '__main__':
    tags = {'Recommend':'1',
            'Popular':'3',
            'Prompt':'4',
            'Programming':'5',
            'Business':'6',
            'Education':'7',
            'Language':'8',
            'Finance':'9',
            'Books':'10',
            'Health':'11',
            'Entertainment':'12',
            'Kids':'13',
            'Travel':'14',
            'Lifestyle':'15',
            'Roleplay':'16',
            'Other':'17'
    }
    for tag,categoryId in tags.items():
        # if tag == 'Business':
        #     break
        # print(tag,categoryId)
        num = 0
        while True:
            info = infoSpider(num,categoryId,tag)
            num +=1
            if info == 'False':break
