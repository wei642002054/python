import re,json
import uuid
from lxml import etree
from pymysql.converters import escape_string
import requests,urllib3
import time,random
from TestMethod.db.linkMariaDB import MySqlSSH  #httpMethod
from TestMethod.public.HttpU import HttpUtil
from TestMethod.public.initLog import generate_unique_id
proxy = HttpUtil.proxy11
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
class forumRpgSpider():
    def __init__(self):
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
        self.domain = 'forum.rpg.net'
        self.dbThread  = 'rolePlayThread'
        self.dbPost = 'rolePlayPost'
        self.dbImage = 'rolePlayImage'
        self.imgPath = r'E:\Img\forumRpgImg/'
        self.author_location = ''  #发帖人的所属地点，作者栏里面如果不显示就空着
        self.author_joined_time = ''  #发帖人加入论坛的时间，作者栏里面如果不显示就空着
        self.author_description = '' #作者描述
    def downloadImg(self,imgAll,forumUrl,post_id):  #下载图片
        for pictureUrl in imgAll:
            try:
                if 'http' not in pictureUrl: pictureUrl = 'https://' + self.domain + pictureUrl
                if MySqlSSH().fetch_one(self.dbImage,'url',pictureUrl) == '已存在' or 'data:' in pictureUrl: continue
                ImgFileId = ''.join(re.findall('.*(\..*)',pictureUrl)).split('?')[0]
                if '/' in ImgFileId or ''.join(re.findall('\d+',str(ImgFileId),re.S)) not in '':continue
                response = HttpUtil.gain(pictureUrl,self.headers)  #有问题
                if response:
                    imgName = generate_unique_id()+ImgFileId
                    with open(self.imgPath+r"{}".format(imgName),"wb") as f:  # 下载封面
                        f.write(response.content)
                    Img_dict = dict(
                        url=str(pictureUrl),
                        referer=forumUrl,
                        post_id=post_id,
                        local_filename=self.imgPath+imgName,
                    )
                    # print('图片下载-->',Img_dict)
                    MySqlSSH().insertDirect(self.dbImage, Img_dict)
            except Exception as e:
                print(f'下载图片有误->{pictureUrl}',e)
    def startSpider(self):
        urls = 'https://forum.rpg.net/index.php'
        respon = requests.get(url=urls, headers=self.headers, proxies=proxy, timeout=8, verify=False)
        # print(respon.text)
        html = etree.HTML(respon.text)
        uids = html.xpath('//div[@class="node-main js-nodeMain"]/h3/a/@href')
        for uid in uids:
            if 'edited-13-may-2021.140' in uid:continue
            #uid = '/index.php?threads/rpg-net-rules-guidelines-updated-dec-13-2023.835825/'
            url = f'https://forum.rpg.net{uid}'+'page-1'
            self.forumListSpider(url)
    def forumListSpider(self, url):
        print(f'正在获取主程序——>{url}')
        resp = HttpUtil().gain(url, self.headers)
        lxml = etree.HTML(resp.text)
        try:
            subForum = lxml.xpath('//div[@class="p-body-content"]/div/div/div[2][@class="block-container"]/div/div/div//h3/a/@href')
            if subForum and 'page-1' in url:
                for subUrl in subForum:
                    subUrls = 'https://forum.rpg.net' + subUrl + 'page-1'
                    print(f'正在获取分论坛--->{subUrls}')
                    self.forumListSpider(subUrls)
            forumList = lxml.xpath('//div[@class="structItemContainer"]/div/div')
            for i in forumList:
                thread_id = generate_unique_id()  # 生成唯一ID
                title = ''.join(i.xpath('string(./div[2]/div[1]/a[@data-xf-init="preview-tooltip"])')).strip()
                forumUrl = ''.join(i.xpath('string(./div[2]/div[1]/a[@data-xf-init="preview-tooltip"]/@href)')).strip()
                if 'http' not in forumUrl:forumUrl = 'https://' + self.domain + forumUrl
                if MySqlSSH().fetch_one(self.dbThread, 'url', forumUrl) == '已存在': continue
                author = ''.join(i.xpath('string(./div[2]/div[2]/ul[2]/li[1])')).strip()
                # pageNum = str(i.xpath('string(./div[2]/div[2]/span)')).replace('\n','').strip()
                # pageMax = re.findall('\d+',pageNum,re.S)
                # if pageMax:pageNum=pageMax[-1]   #最大页数
                # else:pageNum = 1
                release_time = ''.join(i.xpath('string(./div[2]/div[2]/ul[2]/li[2])')).strip()
                respon = HttpUtil().gain(forumUrl, self.headers)
                html = etree.HTML(respon.text)
                board = ','.join(html.xpath('//div[@class="p-body-inner"]/ul[2]/li//span//text()')).strip()
                data_dict = dict(
                    thread_id=thread_id,
                    domain=self.domain,
                    url=forumUrl,
                    detail_url=forumUrl,
                    title=escape_string(str(title)),
                    release_time=escape_string(str(release_time)),
                    author=author,
                    board=escape_string(str(board)),
                )
                print(data_dict)
                MySqlSSH().insertDirect(self.dbThread, data_dict)
                self.postSpider(forumUrl,thread_id)
        except Exception as e:
            print(f'主程序报错{url}',e)
        #获取下页数据
        page = re.findall('/page-(.*)', url, re.S)
        if page: page = int(page[0])
        if page == 1:
            initialPage = re.findall('\d+', str(lxml.xpath('//ul[@class="pageNav-main"]/li/a/text()')), re.S)
            if initialPage:
                numberPage = int(initialPage[-1])
                for record in range(2, numberPage+1):
                    forumRpg = ''.join(re.findall('(http.*?/page-)', url, re.S)).strip()
                    boardNextUrl = forumRpg + str(record)
                    forumRpgSpider().forumListSpider(boardNextUrl)
    def postSpider(self,forumUrl,thread_id):
        if 'page-' not in forumUrl:forumUrl = forumUrl + 'page-1'
        print(f'正在获取详情：{forumUrl}———>thread_id：{thread_id}')
        respon = HttpUtil().gain(forumUrl, self.headers)
        loser = ''.join(re.findall('<style>.*?</style>', str(respon.text), re.S)).strip()
        html = etree.HTML(respon.text.replace(loser, ''))
        try:
            detailAll = html.xpath('//div[@class="block-body js-replyNewMessageContainer"]/article/div')
            for i in detailAll:
                post_id = generate_unique_id()
                imgOne = i.xpath('./div[1]/section//a/img/@src')
                imgTwo = i.xpath('./div[2]/div//img/@src')
                imgAll = list(set(imgOne + imgTwo))
                if imgAll:  # 下载图片保存入库
                    self.downloadImg(imgAll,forumUrl,post_id)
                release_time = ''.join(i.xpath('string(./div[2]/div/header/ul[1]//time)')).strip()
                post_number = ''.join(i.xpath('string(./div[2]/div/header/ul[2]/li[2]//a)')).replace('#', '').strip()  # 楼
                author = ''.join(i.xpath('string(./div[1]/section/div[2]/h4[@class="message-name"]//span)')).strip()
                author_location = self.author_location
                author_joined_time= self.author_joined_time
                autUrl = ''.join(i.xpath('./div[1]/section/div[2]/h4[@class="message-name"]//a/@href')).strip()
                if 'http' not in autUrl:autUrl = 'https://' + self.domain + autUrl
                if autUrl:  #获取所在地和加入论坛的时间
                    resp = HttpUtil().gain(autUrl, self.headers)
                    if resp:
                        lxml = etree.HTML(resp.text)
                        author_location = ''.join(lxml.xpath('//div[@class="memberHeader-blurb"][1]/a//text()')).strip()
                        author_joined_time = ''.join(lxml.xpath('//div[@class="memberHeader-blurb"][2]/dl[1]/dd/time//text()')).strip()
                content = etree.tostring(i, encoding='utf-8').decode()
                content_text = ''.join(i.xpath('string(./div[2]/div[1]//div[@class="bbWrapper"])')).strip()
                data_dict = dict(
                    thread_id=thread_id,
                    domain=self.domain,
                    url=forumUrl,
                    post_id=post_id,
                    post_number=post_number,
                    author_description=self.author_description,
                    release_time=escape_string(str(release_time)),
                    author=escape_string(str(author)),
                    content=escape_string(str(content)),
                    characters='',
                    author_joined_time=escape_string(str(author_joined_time)),
                    author_location=escape_string(str(author_location)),
                    finally_compileTime='',
                    content_text=escape_string(str(content_text)),
                )
                # print(data_dict)
                MySqlSSH().insertDirect(self.dbPost, data_dict)
        except Exception as e:
            print(f'详情报错{forumUrl}',e)
        # #获取下页数据
        page = re.findall('page-(.*)', forumUrl, re.S)
        if page: page = int(page[0])
        if page == 1:
            maxPage =  re.findall('\d+',str(html.xpath('//ul[@class="pageNav-main"]/li/a//text()')),re.S)
            if maxPage:
                numbers = int(maxPage[-1]) + 1
                for record in range(2, numbers):
                    incomplete = ''.join(re.findall('(http.*?page-)', forumUrl, re.S)).strip()
                    perfectly = incomplete + str(record)
                    self.postSpider(perfectly,thread_id)
if __name__ == '__main__':
    # pp = '666'
    # url = 'https://forum.rpg.net/index.php?forums/the-starting-gate-new-player-gm-help.176/page-1'
    # lurl = 'https://forum.rpg.net/index.php?threads/updated-rules-and-guidelines.836040/'
    forum = forumRpgSpider()
    forum.startSpider() #开始
    # forum.forumListSpider(url)  #主列表
    # forum.postSpider(lurl,pp) #详情列表

