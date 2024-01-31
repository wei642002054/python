import re,json
import uuid
from multiprocessing.pool import Pool,ThreadPool
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
class searchRoleSpider():
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
        self.domain = 'rpol.net'
        self.dbThread  = 'rolePlayThread'
        self.dbPost = 'rolePlayPost'
        self.dbImage = 'rolePlayImage'
        self.imgPath = r'E:\Img\searchRoleImg/' #/mnt/yande/forumsImg/
        self.author_location = ''  #发帖人的所属地点，作者栏里面如果不显示就空着
        self.author_joined_time = ''  #发帖人加入论坛的时间，作者栏里面如果不显示就空着
    def downloadImg(self,imgAll,forumUrl,post_id):  #下载图片
        for pictureUrl in imgAll:
            try:
                if 'http' not in pictureUrl: pictureUrl = 'https://' +self.domain + pictureUrl
                if 'data:' in pictureUrl or MySqlSSH().fetch_one(self.dbImage,'url',pictureUrl) == '已存在': continue
                ImgFileId = ''.join(re.findall('.*(\..*)',pictureUrl)).split('?')[0]
                if '/' in ImgFileId or ''.join(re.findall('\d+',str(ImgFileId),re.S)) not in '':continue
                response = HttpUtil.gain(pictureUrl,self.headers)  #有问题
                if response:
                    imgName = generate_unique_id()+ImgFileId
                    with open(self.imgPath+r"{}".format(imgName),"wb") as f:  # 下载封面
                        f.write(response.content)
                    f.close()
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
        url = 'https://rpol.net/?search='
        respon = requests.get(url=url,headers=self.headers,proxies=proxy,timeout=8,verify=False)
        html = etree.HTML(respon.text)
        uids = html.xpath('//form/div[3]/div')
        genreData = []
        for x in uids[:-1]:
            genre = ''.join(x.xpath('string(./label)')).strip()
            uid = ''.join(x.xpath('./label/input[@type="checkbox"]/@value')).strip()
            # print(f'正在获取{uid}----->{genre}')
            url = f'https://rpol.net/?sa=1&rp=1&match=all&sort=alphabetical&search=search&af_general=1&af_mature=1&af_adult=1&af_sowner=1&genre[]={uid}&p=0'
            genreData.append(dict(url=url, gameType=genre))  #进程参数
            # self.gameSearchSpider(url,genre)
        return genreData
    def gameSearchSpider(self,url,gameType):
        print(f'正在获取-->{gameType}<--类型url为——>{url}')
        respon = HttpUtil().gain(url, self.headers)
        try:
            lxml = etree.HTML(respon.text)
            urlAll = lxml.xpath('//div[@id="mainsticky"]/ul/li/div[1]/a/@href')
            for uid in urlAll:
                lurl = 'https://'+self.domain + uid +'&threadpage=1'
                self.rolePlayerSpider(lurl,gameType)
            # 获取下页数据
            initialPage = ''.join(lxml.xpath('//*[@id="mainsticky"]/div/a/text()')).strip()
            if initialPage and 'Next' in initialPage:
                numberPage = int(re.findall('(http.*?&p=(.*))', url, re.S)[0][-1]) + 1
                writer = ''.join(re.findall('(http.*?&p=)', url, re.S)).strip()
                boardNextUrl = writer + str(numberPage)
                searchRoleSpider().gameSearchSpider(boardNextUrl, gameType)
        except Exception as e:
            print('类型程序报错：',e)
    def rolePlayerSpider(self,lurl,gameType):
        print(f'正在获取主程序{gameType}——>{lurl}')
        respon = HttpUtil().gain(lurl, self.headers)
        try:
            lxml = etree.HTML(respon.text)
            forumList = lxml.xpath('//section[@class="gamemenu"]/ul/li')
            for i in forumList[1:]:  #url  //section[@class="gamemenu"]/ul/li/div[2]/div/a/@href
                thread_id = generate_unique_id()  # 生成唯一ID
                roleUrl = ''.join(i.xpath('./div[2]/div/a/@href')).split('&date=')[0].strip()
                if 'http' not in roleUrl: roleUrl = 'https://' + self.domain + roleUrl + '&msgpage=1'
                print('-----------------------(ノ_；＼( ｀ロ´)／报仇！',roleUrl)
                if MySqlSSH().fetch_one(self.dbThread, 'url', roleUrl) == '已存在': continue
                title = ''.join(i.xpath('string(./div[2]/div/a)')).strip()
                author = ''.join(i.xpath('./div[4]/div/text()')).replace('\n','').strip()
                if author:author = author.split('with')[0].replace('by','').strip()
                print('*****************’哇凸(艹皿艹 )')
                resp = HttpUtil().gain(roleUrl, self.headers)
                release_time=''
                if resp:
                    html = etree.HTML(resp.text)
                    release_time = ','.join(html.xpath('//div[@class="message"][1]/div[1]/div/text()')).replace('\n','').strip()
                data_dict = dict(
                    thread_id=thread_id,
                    domain=self.domain,
                    url=roleUrl,
                    detail_url=roleUrl,
                    title=escape_string(str(title)),
                    release_time=escape_string(str(release_time)),
                    author=escape_string(str(author)),
                    board=escape_string(str(gameType)),
                )
                print(data_dict)
                MySqlSSH().insertDirect(self.dbThread, data_dict)
                self.postSpider(roleUrl, thread_id)
            #  下页逻辑  threadpage=1
            page = re.findall('page=(.*)', lurl, re.S)
            if page: page = int(page[0])
            if page == 1:
                initialPage = re.findall('\d+',str(lxml.xpath('//section[@class="gamemenu"]/div[1]/ul/li[1]/text()')).split('of')[-1], re.S)
                if initialPage:
                    numberPage = int(initialPage[-1])
                    for record in range(2, numberPage + 1):
                        writer = ''.join(re.findall('(http.*?page=)', lurl, re.S)).strip()
                        boardNextUrl = writer + str(record)
                        searchRoleSpider().rolePlayerSpider(boardNextUrl, gameType)
        except Exception as e:
            print(f'主程序报错{lurl}',e)
    def postSpider(self,roleUrl, thread_id):
        if '&msgpage=' not in roleUrl: roleUrl = roleUrl + '&msgpage=1'
        print(f'正在获取详情：{roleUrl}———>thread_id：{thread_id}')
        respon = HttpUtil().gain(roleUrl, self.headers)
        try:
            html = etree.HTML(respon.text)
            detailAll = html.xpath('//div[@class="message"]')
            for i in detailAll:
                post_id = generate_unique_id()
                imgOne = i.xpath('./div[@class="messagedetails"]//img/@src')
                imgTwo = i.xpath('./div[@class="messagecontent"]//img/@src')
                imgAll = list(set(imgOne + imgTwo))
                if imgAll:  # 下载图片保存入库
                    self.downloadImg(imgAll, roleUrl, post_id)
                release_time = ' '.join(i.xpath('./div[@class="messagedetails"]/div[1]/text()')).replace('\n','').strip()
                layer_number = len(i.xpath('./div[@class="messagecontent"]/div[1]/ul/li'))
                post_number = ''.join(i.xpath(f'string(./div[@class="messagecontent"]/div[1]/ul/li[{layer_number}])')).split('#')[-1].strip()  # 楼
                author = ''.join(i.xpath('string(./div[1]/span[@class="messageauthor"])')).strip()
                author_description = ','.join(i.xpath('./div[1]/div[1]/div[@class="charbiolines"]/div/text()')).strip()
                content = etree.tostring(i, encoding='utf-8').decode()
                content_text = ''.join(i.xpath('string(./div[@class="messagecontent"])')).strip()
                data_dict = dict(
                    thread_id=thread_id,
                    domain=self.domain,
                    url=roleUrl,
                    post_id=post_id,
                    post_number=post_number,
                    author_description=escape_string(str(author_description)),
                    release_time=escape_string(str(release_time)),
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
            # #获取下页数据
            page = re.findall('page=(.*)', roleUrl, re.S)
            if page: page = int(page[0])
            if page == 1:
                maxPage = re.findall('\d+',str(html.xpath('//div[@class="topthreadnav"]/ul/li[1]/text()')).split('of')[-1],re.S)
                if maxPage:
                    numbers = int(maxPage[-1]) + 1
                    for record in range(2, numbers):
                        incomplete = ''.join(re.findall('(http.*?page=)', roleUrl, re.S)).strip()
                        perfectly = incomplete + str(record)
                        self.postSpider(perfectly, thread_id)
        except Exception as e:
            print(f'详情报错{roleUrl}',e)

def get_list(detailed):
    url = detailed['url']
    gameType = detailed['gameType']
    searchRoleSpider().gameSearchSpider(url, gameType)
if __name__ == '__main__':
    # gameType = 'Sci-Fi' # Sci-Fi Survival
    # urls = 'https://rpol.net/?sa=1&rp=1&match=all&sort=alphabetical&search=search&af_general=1&af_mature=1&af_adult=1&af_sowner=1&genre[]=11&p=0'
    # url = 'https://rpol.net/game.php?gi=72850&date=1703640243&threadpage=1'
    # lurl = 'https://rpol.net/display.cgi?gi=19331&ti=21&date=1288318891&msgpage=1'
    searchRole = searchRoleSpider()
    # searchRole.startSpider()
    # searchRole.gameSearchSpider(urls,gameType)  #搜索后 返回的url列表
    # searchRole.rolePlayerSpider(url,gameType)  #主程序url
    # searchRole.postSpider(lurl,'114455')  #获取详情楼  信息
     ##    开启池子
    celebrity_all = searchRole.startSpider()
    print(len(celebrity_all),celebrity_all)
    # pool = Pool(processes=4)  #进程
    pool = ThreadPool(8) # 线程
    pool.map(get_list, celebrity_all)
    pool.close()
    pool.join()