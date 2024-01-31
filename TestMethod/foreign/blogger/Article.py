import newspaper,requests
from lxml import etree
import random,re
from newspaper import Article
from TestMethod.db.linkMariaDB import MySqlSSH
from TestMethod.public.HttpU import HttpUtil
class ArticleSpider():
    def __init__(self):
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
        self.headers = {
            "User-Agent": random.choice(user_agent)
        }
    def spider_article_information(self,articleUrl,mistake):
        try:  #  language='zh'  匹配中文
            respons = requests.get(url=articleUrl, headers=self.headers, proxies=self.proxy, verify=False)
            html = etree.HTML(respons.text)
            # print(respons.text)
            '//div//p//text()'
            # content = ''.join(html.xpath('//div//p//text()'))
            content = ''.join(re.findall('div class="(\w+-\w+ e-content)', str(respons.text), re.S)).strip()
            Text = ''.join(html.xpath(f'string(//div[@class="{content}"])')).strip()
            if len(Text)<1:
                Text = ''.join(html.xpath('//div//p//text()')).strip()
            print('结果-->', Text)
        # 'string(//div[@class="post-content e-content"])'
            article = Article(articleUrl, proxies=self.proxy, memoize_articles=False)
            article.download()
            article.parse()
            # print(article.html)
            print('******' * 5)
            print(article.url)
            print("Title:", article.title)
            # print("Author:", article.authors)
            # print("Publish Date:", article.publish_date)
            # print("Text:", article.text)
            # data_dict = dict(
            #     articleUrl=articleUrl,
            #     html=article.html,
            #     title=article.title,
            #     authors=article.authors,
            #     publish_date=article.publish_date,
            #     articleText=article.text
            # )
            # print(data_dict)
            # print(f'正在插入')
            # MySqlSSH().conn_mysql('articleDetails', data_dict,articleUrl)
        except Exception as e:
            print(e)
            mistake +=1
            url = input('url有误请重新输入(鼠标放在-->{}然后按Enter确认):')
            if mistake == 3:
                print('输入次数过多||程序有BUG-->程序退出')
                exit()
            ArticleSpider().spider_article_information(url,mistake)
if __name__ == '__main__':
    # https://taresky.com/copyfromchatgpt
    # url = 'https://maxlv.net/blog/china-ev-av-solution/'
    # 匹配不到
    # 'https://laike9m.com/blog/rss/ '
    mistake = 0
    url = input('请输入详情页url(鼠标放在-->{}然后按Enter确认):')
    result = ArticleSpider()
    result.spider_article_information(url,mistake)