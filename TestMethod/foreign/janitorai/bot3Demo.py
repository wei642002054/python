import random
import re
import time
import requests
from lxml import etree
from curl_cffi import requests
from fake_useragent import UserAgent
from multiprocessing.pool import Pool
from pymysql.converters import escape_string
from TestMethod.db.linkMariaDB import MySqlSSH
from TestMethod.public.HttpU import HttpUtil
class BotSpider(object):
    def __init__(self):
        self.headers = {
            'Accept':'application/json, text/plain, */*',
            'User-Agent':UserAgent().random,
        }
        self.proxy = HttpUtil.proxy11
    def initialSpider(self,page):
        params = {
            'page': str(page),
            'is_nsfw': '0',
        }
        url = 'https://bot3.ai/en'
        print(f'✨✨---正在获取第{page}页---✨✨')
        try:
            response = requests.get(url=url, params=params,proxies=self.proxy, headers=self.headers)
            # print(response.text)
            if response:
                html = etree.HTML(response.text)
                detailsUid = html.xpath('//main/div[2]/a/@href')
                # print('loser',detailsUid)
                self.resultSpider(detailsUid)
        except:
            print(f'---重新获取这页----{page}')
            self.initialSpider(page)
    def resultSpider(self,UIdAll):
        for uId in UIdAll:
            try:
                uuid = f'https://bot3.ai{uId}'
                resp = requests.get(url=uuid,timeout=8,proxies=self.proxy, headers=self.headers,verify=False)
                # print(resp.status_code)
                if resp:
                    lxml = etree.HTML(resp.text)
                    ImgLink = ''.join(lxml.xpath('string(//main/img/@src)')).strip()
                    imgId = ''.join(re.findall('bot/(.*)',str(uId),re.S)).strip()
                    ImgResp = HttpUtil().gain(ImgLink, self.headers)
                    with open(r"E:\bot3Img/{}.jpg".format(imgId), "wb") as f:  # 下载封面
                        f.write(ImgResp.content)
                    title = ''.join(lxml.xpath('string(//div[@class="flex items-center"]/h2)')).strip()
                    tags = '、'.join(lxml.xpath('//div[@class="mt-2.5 md:flex md:justify-between"]/ul/li/span/text()')).strip()
                    creator = ''.join(lxml.xpath('string(//div[@class="flex items-center"]/a)')).split(':')[-1].strip()
                    intro = ''.join(lxml.xpath('string(//div[@class="text-[#9a9a9a] font-medium my-8 md:my-10 whitespace-pre-line"])')).strip()
                    description = ''.join(lxml.xpath('string(//div[@class="md:max-w-[745px] flex-1"]/div[5]/div[2])')).strip()
                    personality = ''.join(lxml.xpath('string(//div[@class="md:max-w-[745px] flex-1"]/div[6]/div[2])')).strip()
                    firstMessage = ''.join(lxml.xpath('string(//div[@class="md:max-w-[745px] flex-1"]/div[7]/div[2])')).strip()
                    examplesDialogue = ''.join(lxml.xpath('string(//div[@class="md:max-w-[745px] flex-1"]/div[8]/div[2])')).strip()
                    scenario = ''.join(lxml.xpath('string(//div[@class="md:max-w-[745px] flex-1"]/div[9]/div[2])')).strip()
                    data_dict = dict(
                        url = uuid,
                        imgLink = ImgLink,
                        title=title,
                        tags=escape_string(str(tags)),
                        creator=creator,
                        intro=escape_string(str(intro)),
                        description=escape_string(str(description)),
                        personality=escape_string(str(personality)),
                        firstMessage=escape_string(str(firstMessage)),
                        examplesDialogue=escape_string(str(examplesDialogue)),
                        scenario=escape_string(str(scenario)),
                        html = escape_string(str(resp.text))
                    )
                    # print(data_dict)
                    MySqlSSH().execute_sql('bot3Data', data_dict, uuid)
            except:
                print('Loser-->',uuid)
if __name__ == '__main__':
    sharp = BotSpider()
    po = Pool(2) # 定义一个进程池，最-大进程数2
    print('✨✨---BeginProcedur---✨✨')
    for i in range(1, 468):#458
    # Pool().apply_async(要调用的目标,(传递给目标的参数元祖,))
        po.apply_async(sharp.initialSpider, (i,))  #每次循环将会用空闲出来的子进程去调用目标
    po.close()# 关闭进程池，关闭后po不再接收新的请求
    po.join()# 等待po中所有子进程执行完成，必须放在close语句之后
    print("-----end-----")



