import re,json
import uuid
from multiprocessing.pool import Pool,ThreadPool
import PyPDF2
from bs4 import BeautifulSoup
from lxml import etree
from pymysql.converters import escape_string
import requests,urllib3
import time,random
import pdfplumber
from TestMethod.db.linkMariaDB import MySqlSSH  #httpMethod
from TestMethod.public.HttpU import HttpUtil
from fake_useragent import UserAgent
from TestMethod.public.initLog import generate_unique_id
proxy = HttpUtil.proxy11
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
class simplySpider:
    def __init__(self):
        self.proxy= {
            "https": "127.0.0.1:7890",
            "http": "127.0.0.1:7890"
            }
        self.domain = 'www.simplyscripts.com'
        self.head = {
            'Cookie':'sucuri_cloudproxy_uuid_34c0152b9=9f015579541fa5888c5ef621aa887ff1',
            'Upgrade-Insecure-Requests':'1',
            'Sec-Ch-Ua':'"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.headers={'user-agent':UserAgent().random}
        self.pdfPath = 'E:\downF\pdfFile/'
        self.dbName = 'screenPlays'
    def startSpider(self):
        urls = 'https://www.simplyscripts.com/movie-screenplays.html'
        # url = 'http://www.scifiscripts.com/scripts/2001.txt'
        resp = HttpUtil().ggg(urls, self.head)
        lxml = etree.HTML(resp.text)
        infoAll = lxml.xpath('//div[@id="movie_wide"]//p/a[1]')
        num = 0
        for i in infoAll:
            try:
                num +=1  #1597
                if num >1597:
                    url = ''.join(i.xpath('./@href')).strip()
                    print(f'正在獲取-->{url}')
                    if MySqlSSH().fetch_one(self.dbName, 'url', url) == '已存在': continue
                    content = url.split('/')[-1]
                    playName = ''.join(i.xpath('./text()')).strip() + 'unspecified draft'
                    if '.pdf' in url or '.PDF' in url:
                        content_text = self.pdfDownSpider(url)
                        if len(content_text) <1:continue
                        data_dict = dict(
                            url=url,
                            playName=playName,
                            domain = self.domain,
                            content_text=escape_string(str(content_text)),
                            fileName=escape_string(str(content)),)
                        MySqlSSH().insertDirect(self.dbName, data_dict)
                        continue
                    if 'Casino-Royale' in url or '.doc' in url or '.docx' in url:continue
                    respon = HttpUtil().ggg(url, self.headers)
                    html = etree.HTML(respon.text)
                    content_text = ''.join(html.xpath('//div[@class="container"]//text()')).strip()
                    if len(content_text) <1:content_text = ''.join(html.xpath('//div[@class="Section1"]//text()')).strip()
                    if len(content_text) < 1:content_text = ''.join(html.xpath('string(//tt)')).strip()
                    if len(content_text) < 1:content_text = ''.join(html.xpath('string(//body)')).strip()
                    if 'div.' in content_text or len(content_text) < 1:continue
                    content = respon.text
                    data_dict = dict(
                        url=url,
                        playName=playName,
                        domain=self.domain,
                        content_text=escape_string(str(content_text)),
                        content=escape_string(str(content)), )
                    MySqlSSH().insertDirect(self.dbName, data_dict)
            except Exception as e:
                print(e)
    def pdfDownSpider(self,pdfUrl):   #//tt  //pre
        try:
            fileName = pdfUrl.split('/')[-1]
            pdfresp = HttpUtil().ggg(pdfUrl, self.headers)
            with open(self.pdfPath+fileName,'wb') as f:
                f.write(pdfresp.content)
            print('文件下载完毕')
            local = self.pdfPath+fileName
            with pdfplumber.open(local) as pdf:
                page01 = pdf.pages[0]  # 指定页码
                num_pages = len(pdf.pages)  # 页码总数
                content = ''
                for page_num in range(num_pages):  # 提取所有页
                    page = pdf.pages[page_num]
                    text = page.extract_text()  # 提取文本
                    content+=text
                # print(content)
                if content:
                    return content
            return ''
        except Exception as e:
            return ''
        finally:f.close()
if __name__ == '__main__':
    pdfurl = 'http://www.horrorlair.com/scripts/Zombieland.pdf'
    simp = simplySpider()
    simp.startSpider()
    # simp.pdfDownSpider(pdfurl)


