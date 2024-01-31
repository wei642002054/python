import re,json
import uuid
from lxml import etree
from pymysql.converters import escape_string
import requests,urllib3
import time,random
from newspaper import Article
from TestMethod.db.linkMariaDB import MySqlSSH  #httpMethod
from TestMethod.public.HttpU import HttpUtil
from TestMethod.public.initLog import generate_unique_id
proxy = HttpUtil.proxy11
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
class rolePlayingSpider():
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
        self.domain = 'elliquiy.com'
        self.dbThread  = 'rolePlayThread'
        self.dbPost = 'rolePlayPost'
        self.dbImage = 'rolePlayImage'
        self.imgPath = r'E:\Img\elliquiyImg/'
        self.author_location = ''  #发帖人的所属地点，作者栏里面如果不显示就空着
        self.author_joined_time = ''  #发帖人加入论坛的时间，作者栏里面如果不显示就空着
    def downloadImg(self,imgAll,floorUrl,post_id):  #下载图片
        for pictureUrl in imgAll:
            try:
                if 'http' not in pictureUrl: pictureUrl = 'https://' + self.domain + pictureUrl
                if MySqlSSH().fetch_one(self.dbImage,'url',pictureUrl) == '已存在' or 'data:' in pictureUrl: continue
                ImgFileId = ''.join(re.findall('.*(\..*)',pictureUrl))
                response = HttpUtil.gain(pictureUrl,self.headers)
                if response:
                    imgName = generate_unique_id()+ImgFileId
                    with open(self.imgPath+r"{}".format(imgName),"wb") as f:  # 下载封面
                        f.write(response.content)
                    # pictureName.append(dict(pictureUrl=pictureUrl, imgName=imgName))
                    Img_dict = dict(
                        url=str(pictureUrl),
                        referer=floorUrl,
                        post_id=post_id,
                        local_filename=self.imgPath+imgName,
                    )
                    # print('图片下载-->',Img_dict)
                    MySqlSSH().insertDirect(self.dbImage, Img_dict)
            except Exception as e:
                print(f'下载图片有误->{pictureUrl}',e)
    def beginSpider(self):
        url = 'https://elliquiy.com/forums/index.php'
        respon = requests.get(url=url,headers=self.headers,proxies=proxy,timeout=8,verify=False)
        # print(respon.text)
        html = etree.HTML(respon.text)
        uids = html.xpath('//a[@class="subject mobile_subject"]/@href')
        for uid in uids:
            if 'board=697.0' in uid:continue
            self.firstSpider(uid)
    def firstSpider(self,url):
        print(f'正在获取主程序列表——>{url}')
        resp = HttpUtil().gain(url, self.headers)
        lxml = etree.HTML(resp.text)
        try:
            # dataAll = lxml.xpath('//div[@class="windowbg sticky"]')
            #  //div[@class="message_index_title"]  50  外层  内侧25  楼 25
            subForum = lxml.xpath('//div[@id="main_content_section"]/div[2]/div/div[@class="info"]/a/@href')
            if subForum:
                for subUrl in subForum:
                    if 'http' not in subUrl:subUrl = 'https://elliquiy.com/' + subUrl
                    print(f'正在获取分论坛--->{subUrl}')
                    self.firstSpider(subUrl)
            dataAll = lxml.xpath('//div[@id="topic_container"]/div')
            for i in dataAll:
                thread_id = generate_unique_id()  # 生成唯一ID
                detailUid = ''.join(i.xpath('./div[2]/div[1]/div[2]/span//a/@href')).strip()
                PHPSESSID = ''.join(re.findall('PHPSESSID.*?&',detailUid,re.S)).strip()
                uurl = detailUid.replace(PHPSESSID,'').strip() #根据URL去重  因为PHPSESSID每次都变
                if MySqlSSH().fetch_one(self.dbThread,'url',uurl) == '已存在': continue
                title = ''.join(i.xpath('./div[2]/div[1]/div[2]/span//a/text()')).strip()
                authorTime = i.xpath('./div[4]/p/a//text()')
                author = ''
                release_time = ''
                if authorTime:
                    release_time = authorTime[0]  #有问题
                    if ':' not in release_time:release_time=authorTime[0]+authorTime[1]
                    author = authorTime[-1]
                # print(title,'----',release_time)
                respon = HttpUtil().gain(detailUid, self.headers)
                html = etree.HTML(respon.text)
                board = ''.join(html.xpath('//div[@id="inner_section"]/div[3]/ul/li//span//text()')).replace('►',',').strip()
                data_dict = dict(
                    thread_id=thread_id,
                    domain=self.domain,
                    url=uurl,
                    detail_url = detailUid,
                    title=escape_string(str(title)),
                    release_time=escape_string(str(release_time)),
                    author=author,
                    board=escape_string(str(board)),
                )
                print(data_dict)
                # MySqlSSH().insertDirect(self.dbThread, data_dict)
                # rolePlayingSpider().nextInfoSpider(detailUid,thread_id)  #获取详情页
            #  获取下页数据
            page = re.findall('board=.*?\.(.*)',url,re.S)
            if page:page = int(page[0])
            if page == 0:
                initialPage = re.findall('\d+',str(lxml.xpath('//div[@class="pagelinks floatleft"]/a/text()')),re.S)
                if initialPage:
                    numberPage = int(initialPage[-1])
                    for record in range(1,numberPage):
                        page += 50
                        elliquiy = ''.join(re.findall('(http.*?board=.*?)\.',url,re.S)).strip()
                        boardNextUrl = elliquiy+'.'+str(page)
                        rolePlayingSpider().firstSpider(boardNextUrl)
        except Exception as e:
            print(f'主列表程序错误———>{url}',e)
    def nextInfoSpider(self,floorUrl,thread_id):
        print(f'正在获取：{floorUrl}———>thread_id：{thread_id}')
        respon = HttpUtil().gain(floorUrl, self.headers)
        html = etree.HTML(respon.text)
        # print(respon.text)
        try:
            detailAll = html.xpath('//div[@id="forumposts"]/form/div')
            num = 0
            for i in detailAll:
                num +=1
                post_id = generate_unique_id()
                imgOne = i.xpath('div[1]/div[1]/ul/li//img/@src')
                imgTwo = i.xpath('./div[1]/div[3]/div[@class="signature"]//img/@src')
                imgThree = i.xpath('./div[1]/div[2]/div[2]/div//img/@src')
                imgAll = list(set(imgOne + imgTwo + imgThree))
                if imgAll:  # 下载图片保存入库
                    self.downloadImg(imgAll,floorUrl,post_id)
                release_time = ''.join(i.xpath('./div[1]/div[2]/div[1]/div[2]/a/text()')).strip() # 时间
                post_number = ''.join(i.xpath('./div[1]/div[2]/div[1]/span/text()')).replace('#','').strip()  #楼
                author = ''.join(i.xpath('./div[1]/div[1]/h4/a/text()')).strip()
                author_description = ''.join(i.xpath('string(./div[1]/div[1]/ul/li[@class="title"])')).strip()
                content = etree.tostring(i, encoding='utf-8').decode()
                content_text = ''.join(i.xpath('string(./div[1]/div[2]/div[2]/div)')).strip()
                characters = ''.join(i.xpath('string(./div[1]/div[1]/ul/li[@class="membergroup"])')).strip()
                finally_compileTime = ''.join(i.xpath('string(./div[1]/div[2]/div[1]/div[2]/span[3])')).strip() #最后编辑时间 (有些会为空)
                data_dict = dict(
                    thread_id=thread_id,
                    domain=self.domain,
                    url=floorUrl,
                    post_id=post_id,
                    post_number = post_number,
                    author_description=escape_string(str(author_description)),
                    release_time=escape_string(str(release_time)),
                    author=escape_string(str(author)),
                    content=escape_string(str(content)),
                    characters=escape_string(str(characters)),
                    author_joined_time=self.author_joined_time,
                    author_location=self.author_location,
                    finally_compileTime=finally_compileTime,
                    content_text=escape_string(str(content_text)),
                )
                MySqlSSH().insertDirect(self.dbPost, data_dict)
                # print(num,'---->',data_dict)
            page = re.findall('topic=.*?\.(.*)',floorUrl,re.S)
            if page:page = int(page[0])
            if page == 0:
                initialPage = re.findall('\d+',str(html.xpath('//div[@class="pagelinks floatleft"]/a/text()')),re.S)
                if initialPage:
                    numberPage = int(initialPage[-1])
                    for record in range(1,numberPage):
                        page += 25
                        elliquiy = ''.join(re.findall('(http.*?topic=.*?)\.',floorUrl,re.S)).strip()
                        topicNextUrl = elliquiy+'.'+str(page)
                        rolePlayingSpider().nextInfoSpider(topicNextUrl,thread_id)
        except Exception as e:
            print(f'详情页报错-->{floorUrl}',e)
if __name__ == '__main__':
    # lurl = 'https://elliquiy.com/forums/index.php?topic=321771.0'
    # lurl = 'https://elliquiy.com/forums/index.php?topic=344075.0'
    # lurl = 'https://elliquiy.com/forums/index.php?topic=132072.0'
    # url = 'https://elliquiy.com/forums/index.php?topic=348434.0' #4
    # url = 'https://elliquiy.com/forums/index.php?board=376.0' #10
    # url = 'https://elliquiy.com/forums/index.php?PHPSESSID=vo9k52kdlsoh9vlcarqqjpek5f&board=108.0'
    RoleNPC = rolePlayingSpider()
    RoleNPC.beginSpider()
    # RoleNPC.firstSpider(url) # 主列表
    # RoleNPC.nextInfoSpider(lurl,'loser') #楼列表   《主攻》




