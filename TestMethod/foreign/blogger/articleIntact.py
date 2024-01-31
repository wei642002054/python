import re,json
from lxml import etree
from pymysql.converters import escape_string
import requests
import time,random
from newspaper import Article
from TestMethod.db.linkMariaDB import MySqlSSH  #httpMethod
from TestMethod.public.HttpU import HttpUtil
class articleList():
    def __init__(self,url,fileName,page):
        self.proxy11 = {
            "https": "127.0.0.1:7890",
            "http": "127.0.0.1:7890"
        }
        self.proxy = HttpUtil.proxy11
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
        self.url = url
        self.FilePath = 'E:\JsonPath'  #'articleFile'
        self.fileName = fileName
        self.page = page
        self.headers = {
            ""
            "User-Agent": random.choice(user_agent)
        }
    def insertMysql(self,condition,articleUrl,Text,title):  #插入url
        blogger_dict = {
            'blogger': self.fileName,
            'filePath':self.FilePath+'/'+self.fileName+'.json',
            'articleText':escape_string(str(Text)),
            'title':escape_string(str(title)),
            'articleUrl': escape_string(str(articleUrl))
        }
        MySqlSSH().fetch_all('bloggerData_copy1', blogger_dict,condition,articleUrl)
    def downloadJson(self,data_dict):  # 下载json文件
        json_str = json.dumps(data_dict, ensure_ascii=False, indent=2)
        with open(self.FilePath + '\\' + str(self.fileName)+ '.json', mode='a',
                  encoding='utf-8') as f:
            f.write(json_str)
    def spider_article_information(self):   #获取详情页内容
        try:
            startTime = time.time()
            article = Article(self.url,proxies=self.proxy,language='zh', memoize_articles=False)
            article.download()
            article.parse()
            if article.text:
                data_dict = dict(
                    initialUrl = self.url,
                    articleUrl=self.url,
                    html=article.html,
                    title=article.title,
                    authors=article.authors,
                    publish_date=str(article.publish_date),
                    createTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    articleText=article.text
                )
                endTime = time.time()
                infoTime = round(endTime - startTime, 2)
                articleData = {
                    'fileName': str(self.fileName),
                    'page': str(self.page),
                    'wasteTime': str(infoTime) + '秒',
                    'createTime': str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                    'data': data_dict
                }
                if MySqlSSH().fetch_one('bloggerData_copy1', 'articleUrl', self.url) == '未存在':
                    self.downloadJson(articleData)
                self.insertMysql('articleUrl', self.url,article.text,article.title)
                return articleData
            else:
                respons = requests.get(url=self.url, headers=self.headers, proxies=self.proxy, verify=False)
                if respons.status_code == 200:
                    html = etree.HTML(respons.text)
                    content = ''.join(re.findall('div class="(\w+-\w+ e-content)', str(respons.text), re.S)).strip()
                    Text = ''.join(html.xpath(f'string(//div[@class="{content}"])')).strip()
                    if len(Text) < 1:
                        Text = ''.join(html.xpath('//div//p//text()')).strip()
                    data_dict = dict(
                        initialUrl=self.url,
                        articleUrl=self.url,
                        html=article.html,
                        title=article.title,
                        authors=article.authors,
                        publish_date=str(article.publish_date),
                        createTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        articleText=Text
                    )
                    endTime = time.time()
                    infoTime = round(endTime - startTime, 2)
                    articleData = {
                        'fileName': str(self.fileName),
                        'page': str(self.page),
                        'wasteTime': str(infoTime) + '秒',
                        'createTime': str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                        'data': data_dict
                    }
                    if MySqlSSH().fetch_one('bloggerData_copy1', 'articleUrl', self.url) == '未存在':
                        self.downloadJson(articleData)
                    self.insertMysql('articleUrl', self.url,Text,article.title)
                    return articleData
        except Exception as e:
            print('url不能访问')
    def initialSpider(self):
        startTime = time.time()
        resp = requests.get(url=self.url,headers=self.headers,proxies=self.proxy,verify=False)
        lxml = etree.HTML(resp.text)
        urlList = lxml.xpath('//div//a/@href')
        num = 0
        articleDict = []
        print(urlList)
        for articleUrl in urlList:
            if '#' in articleUrl or '/' == articleUrl or '.pptx' in articleUrl or '.pdf' in articleUrl or '.xml' in articleUrl:continue
            urls = ''.join(re.findall('http.*?//.*?/', str(self.url), re.S)).strip()
            if 'http' not in articleUrl:
                if urls == '':urls=self.url
                articleUrl = urls + str(articleUrl)
            if 'http' in articleUrl and urls not in articleUrl:continue
            print(articleUrl)
            if MySqlSSH().fetch_one('bloggerData_copy1','articleUrl',articleUrl)  == '已存在': continue
            num +=1
            print(num,"文章页面url:", articleUrl)
            result = articleList(self.url,self.fileName,self.page).articleSpider(articleUrl)
            if result:
                self.insertMysql('articleUrl',articleUrl,result.get('articleText'),result.get('title'))
                articleDict.append(result)
        endTime = time.time()
        infoTime = round(endTime - startTime, 2)
        data_dict ={
            'fileName':str(self.fileName),
            'page':str(self.page),
            'wasteTime': str(infoTime) + '秒',
            'createTime': str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
            'data':articleDict
        }
        self.downloadJson(data_dict)
        return data_dict
    def articleSpider(self,articleUrl):
        try:
            article = Article(articleUrl,proxies=self.proxy,language='zh', memoize_articles=False)
            article.download()
            article.parse()
            if article.text:
                data_dict = dict(
                    initialUrl = self.url,
                    articleUrl=articleUrl,
                    html=article.html,
                    title=article.title,
                    authors=article.authors,
                    publish_date=str(article.publish_date),
                    createTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    articleText=article.text
                )
                return data_dict
            else:
                respons = requests.get(url=articleUrl, headers=self.headers, proxies=self.proxy, verify=False)
                respons.encoding=respons.apparent_encoding
                if respons.status_code == 200:
                    html = etree.HTML(respons.text)
                    content = ''.join(re.findall('div class="(\w+-\w+ e-content)', str(respons.text), re.S)).strip()
                    Text = ''.join(html.xpath(f'string(//div[@class="{content}"])')).strip()
                    if len(Text) < 1:
                        Text = ''.join(html.xpath('//div//p//text()')).strip()
                    data_dict = dict(
                        initialUrl=self.url,
                        articleUrl=articleUrl,
                        html=article.html,
                        title=article.title,
                        authors=article.authors,
                        publish_date=str(article.publish_date),
                        createTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        articleText=Text
                    )
                    return data_dict
        except Exception as e:
            print('url不能访问')
if __name__ == '__main__':
    # 'https://01.me/'       匹配过多url(有垃圾帖子  最新发布) https://by-igotit.com/
    #匹配不到列表  https://bc-li.github.io/categories/blog/
    url = input('请输入博主列表url(鼠标放在-->{}然后按Enter确认):')
    fileName = input('请输入博主姓名')
    page = input('请输入页码数用来保存')
    articleInfo = articleList(url,fileName,page)
    # articleInfo.initialSpider()  #获取多个url详情内容  urllist
    articleInfo.spider_article_information()  #文章详情url获取单个内容  url
