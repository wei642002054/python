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
class rolePlayerNetSpider():
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
        self.domain = 'role-player.net'
        self.dbThread  = 'rolePlayThread'
        self.dbPost = 'rolePlayPost'
        self.dbImage = 'rolePlayImage'
        self.imgPath = r'E:\Img\rolePlayerNetImg/'
        self.author_location = ''  #发帖人的所属地点，作者栏里面如果不显示就空着
        self.author_joined_time = ''  #发帖人加入论坛的时间，作者栏里面如果不显示就空着
    def downloadImg(self,imgAll,forumUrl,post_id):  #下载图片
        for pictureUrl in imgAll:
            try:
                if 'http' not in pictureUrl: pictureUrl = 'https://' +self.domain + '/forum/'  + pictureUrl
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
        uids = [
            'forumdisplay.php?f=2',
            'forumdisplay.php?f=3',
            'forumdisplay.php?f=4',
            'forumdisplay.php?f=5',
            'forumdisplay.php?f=22',
            'forumdisplay.php?f=6',
            'forumdisplay.php?f=8',
            'forumdisplay.php?f=9',
            'forumdisplay.php?f=10',
            'forumdisplay.php?f=38',
            'forumdisplay.php?f=12',
            'forumdisplay.php?f=13',
            'forumdisplay.php?f=229',
            'forumdisplay.php?f=238',
            'forumdisplay.php?f=286',
            'forumdisplay.php?f=15',
            'forumdisplay.php?f=16',
            'forumdisplay.php?f=17',
            'forumdisplay.php?f=18',
        ]
        for uid in uids:
            url = 'https://' +self.domain + '/forum/' + uid +'&page=1'
            # print(url)
            self.rolePlayerSpider(url)
    def rolePlayerSpider(self,url):
        print(f'正在获取主程序——>{url}')
        respon = HttpUtil().gain(url, self.headers)
        lxml = etree.HTML(respon.text)
        try:
            subForum = lxml.xpath('//div[@id="forumbits"]/ol/li/div/div[1]/div//h2/a/@href')
            if subForum and 'page=1' in url:  # 分论坛
                for subUrl in subForum:
                    subUrls = 'https://' +self.domain + '/forum/' + str(subUrl).split('&s=')[0] + '&page=1'
                    print(f'正在获取分论坛--->{subUrls}')
                    self.rolePlayerSpider(subUrls)
            forumList = lxml.xpath('//div[@id="threadlist"]/form/div[1]/ol/li/div')
            for i in forumList:
                thread_id = generate_unique_id()  # 生成唯一ID
                rolePlaUrl = ''.join(i.xpath('./div//h3/a[@class="title"]/@href')).strip()
                if 'http' not in rolePlaUrl: rolePlaUrl = 'https://' +self.domain + '/forum/' + str(rolePlaUrl).split('&s=')[0]
                if MySqlSSH().fetch_one(self.dbThread, 'url', rolePlaUrl) == '已存在': continue
                title = ''.join(i.xpath('./div//h3/a[@class="title"]/text()')).strip()
                author = ''.join(i.xpath('string(./div//span/a[@class="username understate"])')).strip()
                release_time = ''.join(i.xpath('./div//span/a/@title')).split('on')[-1].strip()
                resp = HttpUtil().gain(rolePlaUrl, self.headers)
                html = etree.HTML(resp.text)
                board = ','.join(html.xpath('//div[@id="breadcrumb"]/ul/li//text()')).strip()
                data_dict = dict(
                    thread_id=thread_id,
                    domain=self.domain,
                    url=rolePlaUrl,
                    detail_url=rolePlaUrl,
                    title=escape_string(str(title)),
                    release_time=escape_string(str(release_time)),
                    author=escape_string(str(author)),
                    board=escape_string(str(board)),
                )
                print(data_dict)
                MySqlSSH().insertDirect(self.dbThread, data_dict)
                self.postSpider(rolePlaUrl, thread_id)
        except Exception as e:
            print(f'主程序报错{url}',e)
        #获取下页数据
        page = re.findall('&page=(.*)', url, re.S)
        if page: page = int(page[0])
        if page == 1:
            initialPage = re.findall('\d+', str(lxml.xpath('//div[@id="above_threadlist"]/div/form/span[1]/a/text()')).split('of')[-1], re.S)
            if initialPage:
                numberPage = int(initialPage[-1])
                for record in range(2, numberPage+1):
                    writer = ''.join(re.findall('(http.*?&page=)', url, re.S)).strip()
                    boardNextUrl = writer + str(record)
                    rolePlayerNetSpider().rolePlayerSpider(boardNextUrl)
    def postSpider(self,rolePlaUrl, thread_id):
        if 'page=' not in rolePlaUrl: rolePlaUrl = rolePlaUrl + '&page=1'
        print(f'正在获取详情：{rolePlaUrl}———>thread_id：{thread_id}')
        respon = HttpUtil().gain(rolePlaUrl, self.headers)
        html = etree.HTML(respon.text)
        try:
            detailAll = html.xpath('//div[@id="postlist"]/ol/li')
            for i in detailAll:
                post_id = generate_unique_id()
                imgOne = i.xpath('./div[2]/div[1]/a/img/@src')
                imgTwo = i.xpath('./div[2]/div[2]/div//img/@src')
                imgAll = list(set(imgOne + imgTwo))
                if imgAll:  # 下载图片保存入库
                    self.downloadImg(imgAll, rolePlaUrl, post_id)
                release_time = ''.join(i.xpath('string(./div[1]/span[1]/span)')).strip()
                post_number = ''.join(i.xpath('string(./div[1]/span[2]/a[1])')).replace('#', '').strip()  # 楼
                author = ''.join(i.xpath('string(./div[2]/div[1]/div[@class="username_container"]//a/strong)')).strip()
                description = ''.join(i.xpath('string(./div[2]/div[1]/dl/dt[3])')).strip()
                author_description = ''
                if 'Favourite Roleplay Genres' == description:author_description = ''.join(i.xpath('string(./div[2]/div[1]/dl/dd[3])')).strip()
                author_joined_time = self.author_joined_time
                author_location = self.author_location
                joinedTime = ''.join(i.xpath('string(./div[2]/div[1]/dl[1]/dt[1])')).strip()
                location = ''.join(i.xpath('string(./div[2]/div[1]/dl[1]/dt[2])')).strip()
                if 'Join Date' == joinedTime or 'Joined' in joinedTime: author_joined_time = ''.join(i.xpath('string(./div[2]/div[1]/dl[1]/dd[1])')).strip()
                if 'Location' in location: author_location = ''.join(i.xpath('string(./div[2]/div[1]/dl[1]/dd[2])')).strip()
                content = etree.tostring(i, encoding='utf-8').decode()
                content_text = ''.join(i.xpath('string(./div[2]/div[2])')).strip()
                data_dict = dict(
                    thread_id=thread_id,
                    domain=self.domain,
                    url=rolePlaUrl,
                    post_id=post_id,
                    post_number=post_number,
                    author_description=escape_string(str(author_description)),
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
            print(f'详情报错{rolePlaUrl}',e)
        # #获取下页数据
        page = re.findall('page=(.*)', rolePlaUrl, re.S)
        if page: page = int(page[0])
        if page == 1:
            maxPage = re.findall('\d+',str(html.xpath('//div[@id="above_postlist"]/div/form/span[1]/a/text()')).split('of')[-1],re.S)
            if maxPage:
                numbers = int(maxPage[-1]) + 1
                for record in range(2, numbers):
                    incomplete = ''.join(re.findall('(http.*?page=)', rolePlaUrl, re.S)).strip()
                    perfectly = incomplete + str(record)
                    self.postSpider(perfectly,thread_id)
if __name__ == '__main__':
    # urls = 'https://role-player.net/forum/forumdisplay.php?f=5&page=1'
    # pp = '556677'
    # lurl = 'https://role-player.net/forum/showthread.php?t=21119&page=3'
    rolePla = rolePlayerNetSpider()
    rolePla.startSpider()
    # rolePla.rolePlayerSpider(urls)
    # rolePla.postSpider(lurl,pp)