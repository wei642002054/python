import requests
import urllib3
import ssl
import re
from multiprocessing import Pool
import os
import random
from lxml import etree
from bs4 import BeautifulSoup
from pymysql.converters import escape_string
from requests.adapters import HTTPAdapter
from TestMethod.db.linkMariaDB import MySqlSSH
from TestMethod.public.HttpU import HttpUtil

urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
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
req_sess = requests.Session()
req_sess.mount('http://', HTTPAdapter(max_retries=10))
req_sess.mount('https://', HTTPAdapter(max_retries=10))
ssl._create_default_https_context = ssl._create_unverified_context
headers = {
    "User-Agent": random.choice(user_agent)
}
proxy = HttpUtil.proxy11
def stratSpider(page):
    Aurl = 'https://yande.re/post'
    params = {
        'page': str(page),
        'tags': 'genshin_impact',
    }
    print(f'正在获取第--->{page}页')
    response = requests.get(url=Aurl,params=params,proxies=proxy,headers=headers,verify=False)
    lxml = etree.HTML(response.text)
    urlId = lxml.xpath('//*[@id="post-list-posts"]/li/div[1]/a/@href')
    num = 0
    for uid in urlId:
        num +=1
        details = f'https://yande.re{uid}'
        resultSpider(num,details)
def resultSpider(num,Rurl):
    response = requests.get(url=Rurl,proxies=proxy,verify=False, headers=headers)
    if response.status_code != 200:
        print(num,'Ip有问题重试获取',Rurl)
        resultSpider(num,Rurl)
    lxml = etree.HTML(response.text)
    invitation = ''.join(lxml.xpath('string(//div[@id="post-view"]/div[3])')).strip()
    if 'Search' in invitation and 'Tags' in invitation:invitation=''
    else:invitation=invitation
    tagHtml = ''.join(re.findall('Tags</h5>(.*?)<span style="display',response.text,re.S))
    html = etree.HTML(tagHtml)
    Tags = ''.join(html.xpath('//li//text()')).strip()
    # SHtml = ''.join(re.findall('Statistics</h5>(.*?)</span></span></li>',response.text,re.S))
    # loser = ''.join(re.findall('<span id="remaining-favs.*?</span>',SHtml,re.S))
    loser = ''.join(re.findall('<span id="remaining-favs.*?</span>',response.text,re.S))
    Resp = response.text.replace(loser,'')
    SHtml = etree.HTML(Resp)
    Statistics = ''.join(SHtml.xpath('string(//*[@id="stats"]/ul)')).strip()
    data_dict = dict(
        invitation=invitation,
        Tags=escape_string(str(Tags)),
        Statistics=escape_string(str(Statistics)),
        url=Rurl,
        HtmlTxt=escape_string(str(response.text))
    )
    MySqlSSH().execute_sql('yandedata',data_dict,Rurl)
    print(f'正在获取第--->{num}个')
if __name__ == "__main__":
    po = Pool(2) # 定义一个进程池，最大进q程数2
    for i in range(868, 911):
    # Pool().apply_async(要调用的目标,(传递给目标的参数元祖,))
    # 每次循环将会用空闲出来的子进程去调用目标
        po.apply_async(stratSpider, (i,))
        # stratSpider(i)
        print("----start----")
        # 关闭进程池，关闭后po不再接收新的请求
    po.close()
    # # 等待po中所有子进程执行完成，必须放在close语句之后
    po.join()
    print("-----end-----")