import re,json
import uuid
from multiprocessing.pool import Pool,ThreadPool

from bs4 import BeautifulSoup
from lxml import etree
from pymysql.converters import escape_string
import requests,urllib3
import time,random
from TestMethod.db.linkMariaDB import MySqlSSH  #httpMethod
from TestMethod.public.HttpU import HttpUtil
from fake_useragent import UserAgent
from TestMethod.public.initLog import generate_unique_id
proxy = HttpUtil.proxy11
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
class gutenbergSpider:
    def __init__(self):
        self.proxy= {
            "https": "127.0.0.1:7890",
            "http": "127.0.0.1:7890"
            }
        self.domain = 'www.gutenberg.org'
        self.headers = {
            'user-agent':UserAgent().random
        }
        self.dbName = 'gutenbergBook'
    def languageCategory(self):
        genreData = []
        languageAll={
        'Chinese':r'/browse/languages/zh',
        'Danish':r'/browse/languages/da',
        'Dutch':r'/browse/languages/nl',
        'English':r'/browse/languages/en',
        'Esperanto':r'/browse/languages/eo',
        'Finnish':r'/browse/languages/fi',
        'French':r'/browse/languages/fr',
        'German':r'/browse/languages/de',
        'Greek':r'/browse/languages/el',
        'Hungarian':r'/browse/languages/hu',
        'Italian':r'/browse/languages/it',
        'Latin':r'/browse/languages/la',
        'Portuguese':r'/browse/languages/pt',
        'Spanish':r'/browse/languages/es',
        'Swedish':r'/browse/languages/sv',
        'Tagalog':r'/browse/languages/tl',
        }
        for language, uids in languageAll.items():
            if 'Chinese' == language or 'Danish' == language or 'Esperanto' == language:continue
            url = 'https://'+self.domain+uids
            genreData.append(dict(url=url, language=language))
        return genreData
    def resultSpider(self,catUid,language):
        try:
            print(f'正在获取--{language}',catUid)
            resp = HttpUtil().gain(catUid, self.headers)
            resLxml = etree.HTML(resp.text)
            detailsUrl = resLxml.xpath('//div[@class="pgdbbylanguage"]//ul/li/a/@href')
            num = 0
            for uid in detailsUrl:
                num +=1
                detail = 'https://'+self.domain+uid
                print('----------------')
                if MySqlSSH().fetch_one(self.dbName, 'url', detail) == '已存在': continue
                tableResp = HttpUtil().gain(detail, self.headers)
                lxml = etree.HTML(tableResp.text)
                href = ''.join(lxml.xpath('//table[@class="files"]//tr[2]/td[2]/a/@href')).strip()
                contentUrl = 'https://' +self.domain+ href
                author = ''.join(lxml.xpath('string(//div[@id="bibrec"]//table//tr[1]/td/a[@itemprop="creator"])')).strip()
                title = ''.join(lxml.xpath('string(//div[@id="bibrec"]//table//tr/td[@itemprop="headline"])')).strip()
                releaseDate = ''.join(lxml.xpath('string(//div[@id="bibrec"]//table//tr/td[@itemprop="datePublished"])')).strip()
                dateModified = ''.join(lxml.xpath('string(//div[@id="bibrec"]//table//tr/td[@itemprop="dateModified"])')).strip()
                respons = HttpUtil().gain(contentUrl, self.headers)
                soup = BeautifulSoup(respons.text, 'lxml')
                [s.extract() for s in soup('section')]  # 去除section标签多余数据
                html = etree.HTML(str(soup))
                content_text = ''.join(html.xpath('string(//body)')).strip()
                data_dict = dict(
                    url=detail,
                    domain=self.domain,
                    author=escape_string(str(author)),
                    title=escape_string(str(title)),
                    language=language,
                    releaseDate=escape_string(str(releaseDate)),
                    dateModified=escape_string(str(dateModified)),
                    content_url=contentUrl,
                    content=escape_string(str(soup)),
                    content_text=escape_string(str(content_text)),
                )
                # print(data_dict)
                MySqlSSH().insertDirect(self.dbName, data_dict)
        except Exception as e:
            print(e)
def get_list(detailed):
    url = detailed['url']
    language = detailed['language']
    gutenbergSpider().resultSpider(url, language)
if __name__ == '__main__':
    url = 'https://www.gutenberg.org/browse/languages/zh'
    king = gutenbergSpider()  #//table[@class="files"]//tr[2]/td[2]/a/@href
    # king.resultSpider(url)  #'string(//body)'
    # king.info()
    celebrity_all = king.languageCategory()
    print(len(celebrity_all))
    pool = Pool(processes=2)  #进程
    # pool = ThreadPool(6) # 线程
    pool.map(get_list, celebrity_all)
    pool.close()
    pool.join()
