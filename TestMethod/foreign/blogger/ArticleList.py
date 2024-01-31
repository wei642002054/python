import re
from lxml import etree
from selenium import webdriver
import requests
import time
import newspaper
from selenium.webdriver.chrome.options import Options
from newspaper import Article
from TestMethod.public.HttpU import HttpUtil
class articleLists():
    def __init__(self):
        self.proxy11 = {
            "https": "127.0.0.1:7890",
            "http": "127.0.0.1:7890"
        }
        self.proxy = HttpUtil.proxy11
    def initialSpider(self,url):
        source = newspaper.build(url,proxies=self.proxy,language='zh', memoize_articles=False)
        source.download()
        # print(source.html)
        source.parse()
        num = 0
        for article in source.articles:
            print('aaaaaa',article.url)
            if '#' in article.url:continue
            num +=1
            # if 'http' not in article.url:
            #     article.url = ''.join(re.findall('http.*?//.*?',str(url)),re.S).strip()+article.url
            print(num,"文章页面url:", article.url)
            articleLists().spider_article_information(article.url)
    def spider_article_information(self,detailsUrl):
        article = Article(detailsUrl,proxies=self.proxy,language='zh', memoize_articles=False)
        article.download()
        # print(article.html)
        article.parse()
        print('******'*5)
        print(article.url)
        print("Title:", article.title)
        print("Author:", article.authors)
        print("Publish Date:", article.publish_date)
        print("Text:", article.text)
        # print("Keywords:", article.keywords)
if __name__ == '__main__':
    # 'https://01.me/'       匹配过多url(有垃圾帖子  最新发布) https://by-igotit.com/
    #匹配不到列表  https://bc-li.github.io/categories/blog/
    url = input('请输入博主列表url(鼠标放在-->{}然后按Enter确认):')
    articleInfo = articleLists()
    articleInfo.initialSpider(url)
