import requests
import urllib3
import time
import random
import asyncio
import cloudscraper
from pymysql.converters import escape_string
from multiprocessing.pool import Pool
from TestMethod.db.linkMariaDB import MySqlSSH
requests.packages.urllib3.disable_warnings()
from curl_cffi import requests
from fake_useragent import UserAgent
from TestMethod.public.HttpU import HttpUtil
urllib3.disable_warnings()
headers = {
    'Accept':'application/json, text/plain, */*',
    'User-Agent':UserAgent().random,
}
def initialSpider(page):
    params = {
        'page': str(page),
        'tag_id': '1',
        'sort': 'popular',
        'mode': 'all',
    }
    print(f'正在获取第{page}页')
    url = 'https://miguel.janitorai.com/characters'
    try:
        TLSAll = ["edge99", "edge101", "chrome99", "chrome100", "chrome101", "chrome104", "chrome107", "chrome110",
                  "chrome99_android", "safari15_3", "safari15_5"]
        proxy = HttpUtil.proxy11
        response = requests.get(url=url, proxies=proxy, params=params, impersonate=random.choice(TLSAll), headers=headers,verify=False)
        # print(response.json())
        if response.status_code == 200:
            result = response.json()['data']
            # print(result)
            resultSpider(result)
    except:
        print(f'重新获取这页----{page}')
        initialSpider(page)
def resultSpider(info):
    for i in info:
        uuid = 'https://miguel.janitorai.com/characters/{}'.format(i['id'])
        resp = HttpUtil().JsonGet(uuid,headers,'avatar')
        info = resp.json()
        imgId = 'https://pics.janitorai.com/bot-avatars/{}'.format(info['avatar'])
        ImgResp = HttpUtil().Rget(imgId, headers)
        # print(ImgResp.content)
        async def read_file():
            with open(r"E:\ImgPath/{}".format(info['avatar']), "wb") as f:  # 下载封面
                await f.write(ImgResp.content)
        data_dict = dict(
            url=uuid,
            avatar=info['avatar'],
            created_at=info['created_at'],
            creator_id=info['creator_id'],
            creator_name=escape_string(str(info['creator_name'])),
            creator_verified=info['creator_verified'],
            description=escape_string(str(info['description'])),
            example_dialogs=escape_string(str(info['example_dialogs'])),
            first_message=escape_string(str(info['first_message'])),
            detail_id=info['id'],
            is_nsfw=info['is_nsfw'],
            is_public=info['is_public'],
            name=escape_string(str(info['name'])),
            personality=escape_string(str(info['personality'])),
            scenario=escape_string(str(info['scenario'])),
            stats=escape_string(str(info['stats'])),
            tag_ids=escape_string(str(info['tag_ids'])),
            tags=escape_string(str(info['tags'])),
            total_chat=info['total_chat'],
            total_message=info['total_message'],
            updated_at=info['updated_at'],
        )
        # print(data_dict)
        MySqlSSH().execute_sql('janitoraiData', data_dict, uuid)

if __name__ == '__main__':
    po = Pool(2) # 定义一个进程池，最大进程数2
    print("----start----")
    for i in range(2942, 2956):
    # Pool().apply_async(要调用的目标,(传递给目标的参数元祖,))
        po.apply_async(initialSpider, (i,))# 每次循环将会用空闲出来的子进程去调用目标
        # stratSpider(i)
    po.close()# 关闭进程池，关闭后po不再接收新的请求
    po.join()# 等待po中所有子进程执行完成，必须放在close语句之后
    print("-----end-----")
