import time
import requests
import urllib3
import ssl
import os
import re
import json
from lxml import etree
import random
from requests.adapters import HTTPAdapter
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
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
req_sess = requests.Session()
req_sess.mount('http://', HTTPAdapter(max_retries=10))
req_sess.mount('https://', HTTPAdapter(max_retries=10))
ssl._create_default_https_context = ssl._create_unverified_context

def createDir(path):  # 创建文件夹
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            print('该文件夹已存在')

    except:
        print('创建文件失败！')
def donwAudio(path,Auid,FileNane):  #保存音频
    music_file = requests.get(url=Auid, headers=headers, verify=False).content
    with open(path + '\\' + FileNane, "wb") as f:
        f.write(music_file)
def result():  #返回结果
    url = 'https://wiki.biligame.com/ys/%E8%A7%92%E8%89%B2%E8%AF%AD%E9%9F%B3'
    response = requests.get(url=url, headers=headers, verify=False)
    html = etree.HTML(response.text)
    titlex = html.xpath('//div[@class="resp-tabs-container"]/div[1]//h2/span[2]/text()')
    num = 0
    for roleType in titlex:
        num += 1
        detailId = html.xpath(f'//div[@class="resp-tabs-container"]/div[1]/div[{str(num)}]/div/div[5]/div[2]//a/@href')
        titleS = html.xpath(f'//div[@class="resp-tabs-container"]/div[1]/div[{str(num)}]/div/div[5]/div[2]//a/@title')
        for uid,title in zip(detailId,titleS):
            uurl = f'https://wiki.biligame.com{uid}'
            print('------>',roleType,title,uid)
            if '.png' in title or '火' == roleType:# or '水' == roleType or '风' == roleType:
                continue
            resp = requests.get(url=uurl, headers=headers, verify=False)
            lxml = etree.HTML(str(resp.text).replace('\n', '').replace('<br />', '').replace('<br/>', '').replace('<br>', ''))
            introduce = lxml.xpath('//*[@id="mw-content-text"]/div/div[3]/div[4]/div[1]/div/div/div[1]/text()')
            if introduce == []:
                continue
            # time.sleep(random.randint(1,3))
            all = lxml.xpath('//div[@class="resp-tabs-container"]/div[1]//table[@class="wikitable"]/tbody')
            dataJson = []
            for i in all:
                introduce = ''.join(i.xpath('./tr[1]/th/text()')).strip()
                china = ''.join(i.xpath('./tr[4]/td/div[1]/text()')).strip()
                Japanese = ''.join(i.xpath('./tr[4]/td/div[2]/text()')).strip()
                English = ''.join(i.xpath('./tr[4]/td/div[3]/text()')).strip()
                Korean = ''.join(i.xpath('./tr[4]/td/div[4]/text()')).strip()
                chinaAudio = ''.join(i.xpath('./tr[3]/td[1]/div/@data-src')).strip()
                if chinaAudio:
                    print('进入chinaAudio下载音频')
                    Chpath = fileN + '\\' + roleType + f'\{title + "_Ch"}'
                    createDir(Chpath)
                    ChFile = ''.join(re.findall('\.com/.*/(.*)', chinaAudio, re.S)).strip()
                    fullPath_Ch = fileAudio + '\\' + roleType + f'\{title + "_Ch"}' + '\\'+ChFile
                    donwAudio(Chpath, chinaAudio, ChFile)
                else:
                    ChFile = ''
                    fullPath_Ch = ''
                JapanAudio = ''.join(i.xpath('./tr[3]/td[2]/div/@data-src')).strip()
                if JapanAudio:
                    print('进入JapanAudio下载音频')
                    Japath = fileN + '\\' + roleType + f'\{title + "_Jap"}'
                    createDir(Japath)
                    JPNFile = ''.join(re.findall('\.com/.*/(.*)', JapanAudio, re.S)).strip()
                    fullPath_Jap = fileAudio + '\\' + roleType + f'\{title + "_Jap"}' + '\\'+JPNFile
                    donwAudio(Japath, JapanAudio, JPNFile)
                else:
                    JPNFile = ''
                    fullPath_Jap = ''
                EngliAudio = ''.join(i.xpath('./tr[3]/td[3]/div/@data-src')).strip()
                if EngliAudio:
                    print('进入EngliAudio下载音频')
                    Enpath = fileN + '\\' + roleType + f'\{title + "_En"}'
                    createDir(Enpath)
                    EnFile = ''.join(re.findall('\.com/.*/(.*)', EngliAudio, re.S)).strip()
                    fullPath_En = fileAudio + '\\' + roleType + f'\{title + "_En"}' + '\\'+EnFile
                    donwAudio(Enpath, EngliAudio, EnFile)
                else:
                    EnFile = ''
                    fullPath_En = ''
                KoreanAudio = ''.join(i.xpath('./tr[3]/td[4]/div/@data-src')).strip()
                if KoreanAudio:
                    print('进入KoreanAudio下载音频')
                    Korepath = fileN + '\\' + roleType + f'\{title + "_Kr"}'
                    createDir(Korepath)
                    KrFile = ''.join(re.findall('\.com/.*/(.*)', KoreanAudio, re.S)).strip()
                    fullPath_Kr = fileAudio + '\\' + roleType + f'\{title + "_Kr"}' + '\\'+KrFile
                    donwAudio(Korepath, KoreanAudio, KrFile)
                else:
                    KrFile = ''
                    fullPath_Kr = ''
                data = {
                    'introduce': introduce,
                    'china': china,
                    'chinaAudio':chinaAudio,
                    'ChFile':ChFile,
                    'fullPath_Ch':fullPath_Ch,
                    'Japanese': Japanese,
                    'JapanAudio':JapanAudio,
                    'JPNFile':JPNFile,
                    'fullPath_Jap':fullPath_Jap,
                    'English': English,
                    'EngliAudio':EngliAudio,
                    'EnFile':EnFile,
                    'fullPath_En':fullPath_En,
                    'Korean': Korean,
                    'KoreanAudio':KoreanAudio,
                    'KrFile':KrFile,
                    'fullPath_Kr':fullPath_Kr
                }
                dataJson.append(data)
            data_dict={
            'tag': roleType,
            'role': title,
            'conversations': dataJson}
            # print(data_dict)
            json_str = json.dumps(data_dict,ensure_ascii=False,indent=2)
            createDir(FileE +'\\'+roleType)
            with open(FileE +'\\'+roleType+'\\'+str(title).replace('语音','')+'.json', mode='w', encoding='utf-8') as f:
                f.write(json_str)
if __name__ == '__main__':
    headers = {
        "User-Agent": random.choice(user_agent)
    }
    fileN = 'D:\yuanshen\Audio'
    fileAudio = 'yuanshen\Audio'
    FileE = r'D:\yuanshen\roleFile'
    result()
