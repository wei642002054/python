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
class rolePlayerGuildSpider():
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
        self.domain = 'roleplayerguild.com'
        self.dbThread  = 'rolePlayThread'
        self.dbPost = 'rolePlayPost'
        self.dbImage = 'rolePlayImage'
        self.imgPath = r'E:\Img\rolePlayerGuild/'
        self.author_location = ''  #发帖人的所属地点，作者栏里面如果不显示就空着
        self.author_joined_time = ''  #发帖人加入论坛的时间，作者栏里面如果不显示就空着
    def downloadImg(self,imgAll,forumUrl,post_id):  #下载图片
        for pictureUrl in imgAll:
            try:
                if 'http' not in pictureUrl: pictureUrl = 'https://www.' +self.domain + '/topics/'  + pictureUrl
                if 'data:' in pictureUrl or MySqlSSH().fetch_one(self.dbImage,'url',pictureUrl) == '已存在': continue
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
        urls = 'https://www.roleplayerguild.com/'
        respon = requests.get(url=urls, headers=self.headers, proxies=proxy, timeout=8, verify=False)
        html = etree.HTML(respon.text)
        uids = html.xpath('//div[@class="row"]/div/h5/a/@href')
        for uid in uids:
            url = 'https://www.' + self.domain + uid +'?page=1'
            self.guildCommunity(url)
    def guildCommunity(self,url):
        print(f'正在获取主程序——>{url}')
        respon = HttpUtil().gain(url, self.headers)
        lxml = etree.HTML(respon.text)
        try:
            forumList = lxml.xpath('//div[@class="list-group"]/div/div[@class="row"]')
            for i in forumList[1:]:
                storey = 0
                thread_id = generate_unique_id()  # 生成唯一ID
                guildUrl = ''.join(i.xpath('./div/h5/a/@href'))
                if 'http' not in guildUrl: guildUrl = 'https://www.' + self.domain + guildUrl
                if MySqlSSH().fetch_one(self.dbThread, 'url', guildUrl) == '已存在': continue
                title = ''.join(i.xpath('./div/h5/a/text()')).strip()
                author = ''.join(i.xpath('string(./div/div[1]/div/a[@style="color: #fff"])')).strip()
                release_time = ''
                resp = HttpUtil().gain(guildUrl, self.headers)
                html = etree.HTML(resp.text)
                board = ','.join(html.xpath('//ol[@class="breadcrumb"]/li//text()')).strip()
                data_dict = dict(
                    thread_id=thread_id,
                    domain=self.domain,
                    url=guildUrl,
                    detail_url=guildUrl,
                    title=escape_string(str(title)),
                    release_time=release_time,
                    author=escape_string(str(author)),
                    board=escape_string(str(board)),
                )
                print(data_dict)
                MySqlSSH().insertDirect(self.dbThread, data_dict)
                self.postSpider(storey,guildUrl, thread_id)
        except Exception as e:
            print(f'主程序报错{url}',e)
        #获取下页数据
        page = re.findall('page=(.*)', url, re.S)
        if page: page = int(page[0])
        if page == 1:
            initialPage = re.findall('\d+', str(lxml.xpath('//ul[@class="pager"][1]/a/text()')).split('of')[-1], re.S)
            if initialPage:
                numberPage = int(initialPage[-1])
                for record in range(2, numberPage+1):
                    writer = ''.join(re.findall('(http.*?page=)', url, re.S)).strip()
                    boardNextUrl = writer + str(record)
                    rolePlayerGuildSpider().guildCommunity(boardNextUrl)
    def postSpider(self,storey,guildUrl, thread_id):
        if '/ooc?page=' not in guildUrl: guildUrl = guildUrl + '/ooc?page=1'
        print(f'正在获取详情：{guildUrl}———>thread_id：{thread_id}')
        respon = HttpUtil().gain(guildUrl, self.headers)
        html = etree.HTML(respon.text)
        try:
            detailAll = html.xpath('//div[@class="container"]/div/div[2]')
            for i in detailAll:
                storey +=1
                post_id = generate_unique_id()
                imgOne = i.xpath('./div/div[2]/div[@class="post-avatar"]//img/@src')
                imgTwo = i.xpath('./div/div[1]/div//img/@src')
                imgAll = list(set(imgOne + imgTwo))
                if imgAll:  # 下载图片保存入库
                    self.downloadImg(imgAll, guildUrl, post_id)
                author = ''.join(i.xpath('string(./div/div[2]/div[@class="user-uname"]/a)')).strip()
                author_description = ''.join(i.xpath('string(./div/div[2]/div[@class="user-custom-title text-muted"])')).strip()
                post_number = storey
                content = etree.tostring(i, encoding='utf-8').decode()
                content_text = ''.join(i.xpath('string(./div[@class="col-sm-10 post-content-wrapper"])')).strip()
                data_dict = dict(
                    thread_id=thread_id,
                    domain=self.domain,
                    url=guildUrl,
                    post_id=post_id,
                    post_number=post_number,
                    author_description=escape_string(str(author_description)),
                    release_time='',
                    author=escape_string(str(author)),
                    content=escape_string(str(content)),
                    characters='',
                    author_joined_time=self.author_joined_time,
                    author_location=self.author_location,
                    finally_compileTime='',
                    content_text=escape_string(str(content_text)),
                )
                # print(data_dict)
                MySqlSSH().insertDirect(self.dbPost, data_dict)
        except Exception as e:
            print(f'详情报错{guildUrl}',e)
        # #获取下页数据
        page = re.findall('page=(.*)', guildUrl, re.S)
        if page: page = int(page[0])
        if page == 1:
            maxPage = re.findall('\d+',str(html.xpath('string(//ul[@class="nav nav-tabs topic-tabs"]/li[1]/a/span)')),re.S)
            if maxPage:
                storeyNum = 0  #楼
                numbers = int(int(str(maxPage[-1]))/20) + 1
                for record in range(2, numbers+1):
                    storeyNum += 20
                    incomplete = ''.join(re.findall('(http.*?page=)', guildUrl, re.S)).strip()
                    perfectly = incomplete + str(record)
                    self.postSpider(storeyNum,perfectly,thread_id)
if __name__ == '__main__':
    # url = 'https://www.roleplayerguild.com/forums/41-roleplaying-discussion?page=1'
    # lurl = 'https://www.roleplayerguild.com/topics/68418-sum-up-your-week-in-roleplaying-in-just-3-words'
    # pp = '112233'
    # storey = 0
    Guild = rolePlayerGuildSpider()
    Guild.startSpider()
    # Guild.guildCommunity(url)
    # Guild.postSpider(storey,lurl,pp)

