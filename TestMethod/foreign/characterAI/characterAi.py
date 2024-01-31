#https://beta.character.ai/
import re
import ssl
import time
import json
import random
import requests
from lxml import etree
from curl_cffi import requests
from pymysql.converters import escape_string
from TestMethod.db.linkMariaDB import MySqlSSH
from TestMethod.public.HttpU import HttpUtil
proxy = HttpUtil.proxy11
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
TLSAll = ["edge99","edge101","chrome99","chrome100","chrome101","chrome104","chrome107","chrome110","chrome99_android","safari15_3","safari15_5"]
cookies = {
    '_legacy_auth0.dyD3gE281MqgISG7FuIXYhL2WEknqZzv.is.authenticated': 'true',
    'auth0.dyD3gE281MqgISG7FuIXYhL2WEknqZzv.is.authenticated': 'true',
    'messages': 'W1siX19qc29uX21lc3NhZ2UiLDAsMjUsIlN1Y2Nlc3NmdWxseSBzaWduZWQgaW4gYXMgNjQyMDAyMDU0QHFxLmNvbS4iLCIiXV0:1r3RJa:FFTqogQwGcnqSAYx-x6LhWzn5qr6BM0JuZFTyy9Y3fk; sessionid=r00i0k8jlwqf4qz2crr0j0j7ldk8dj8s;',
    'sessionid': 'r00i0k8jlwqf4qz2crr0j0j7ldk8dj8s',
    'csrftoken': 'SR94eacJTQSKWFH1Hdv5U4diQae508Y7',
    'AMP_MKTG_39bbdcaee6': 'JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRnd3dy5nb29nbGUuY29tJTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMnd3dy5nb29nbGUuY29tJTIyJTdE',
    '__cf_bm': '7fzFKbMCaaOvo0YVNysAWO0Z9UFJqJCjx_w3O1_HDoY-1700104179-0-AeFaG1PLejU7n79t9FimH9eiT16a+ReUd3L+gtjkWTCWiHmqzfX5wp/w8V8FDHFUWga+NeM7KLXFfMOU3yweHHY=',
    'AMP_39bbdcaee6': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJlOGMyNjBmZC1iYTg0LTRkMGItODY3MS1mNjIzZDA1ZDk5N2MlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjJ1bmRlZmluZWQlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzAwMDk3NzMwNDM5JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcwMDEwNDU3NzQyMyUyQyUyMmxhc3RFdmVudElkJTIyJTNBMjA1JTdE',
    'cf_clearance': 'VAPUNN8F.5DIvFr8Yn_uD8QHFqUvkbohkYeFGc4Kc.w-1700104577-0-1-cc8f5680.ceed3fca.9b8e0960-0.2.1700104577',
}
headers = {          #Token 3338e11836077efae64c373f6786d9e3679f61d5
    'authorization': 'Token 3338e11836077efae64c373f6786d9e3679f61d5',
    'content-type': 'application/json',
    # 'Cookie': 'Cookie:_legacy_auth0.dyD3gE281MqgISG7FuIXYhL2WEknqZzv.is.authenticated=true; auth0.dyD3gE281MqgISG7FuIXYhL2WEknqZzv.is.authenticated=true; messages=W1siX19qc29uX21lc3NhZ2UiLDAsMjUsIlN1Y2Nlc3NmdWxseSBzaWduZWQgaW4gYXMgNjQyMDAyMDU0QHFxLmNvbS4iLCIiXV0:1r3RJa:FFTqogQwGcnqSAYx-x6LhWzn5qr6BM0JuZFTyy9Y3fk; sessionid=r00i0k8jlwqf4qz2crr0j0j7ldk8dj8s; csrftoken=SR94eacJTQSKWFH1Hdv5U4diQae508Y7; AMP_MKTG_39bbdcaee6=JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRnd3dy5nb29nbGUuY29tJTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMnd3dy5nb29nbGUuY29tJTIyJTdE; cf_clearance=VAPUNN8F.5DIvFr8Yn_uD8QHFqUvkbohkYeFGc4Kc.w-1700104577-0-1-cc8f5680.ceed3fca.9b8e0960-0.2.1700104577; __cf_bm=pMOVppw0YAjuNv9_UXcLfAAa1.RbASOpNafisuJWskM-1700105081-0-AT2OYYIPOdLcZuQl/VzGnL7khItiOW5UqjBU6V2s+0OCyr4iWqQSUYLqU2AZzelzCf9b5rFF74gWAec6WthGiwE=; AMP_39bbdcaee6=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJlOGMyNjBmZC1iYTg0LTRkMGItODY3MS1mNjIzZDA1ZDk5N2MlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjIzMDAwOTc3MzYlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzAwMDk3NzMwNDM5JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcwMDEwNTU1MzUyOCUyQyUyMmxhc3RFdmVudElkJTIyJTNBMjEzJTdE',
    # 'origin': 'https://beta.character.ai',
    # 'referer': 'https://beta.character.ai/editing?source=recent-chats&char=1wlJ69BdB0yH0Auc3uOxmdcqG7NF28XiFLhhYv8Zd6o',
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    "User-Agent": random.choice(user_agent)
}
# https://characterai.io/i/400/static/avatars/Heart.png  图片下载地址
def initialSpider():
    url='https://beta.character.ai/chat/curated_categories/characters/'
    # url='https://neo.character.ai/recommendation/v1/trending'
    # url='https://neo.character.ai/recommendation/v1/featured'
    resp = HttpUtil.Rget(url,headers)
    # info = resp.json().get('characters')
    info = resp.json().get('characters_by_curated_category')#.get('Helpers')
    for aiType in info:
    # for i in info:
        for i in info.get(aiType):
            external_id = i.get('external_id')
            imgId = i.get('avatar_file_name')
            resultSpider(external_id,imgId,aiType)
def resultSpider(external_id,imgId,aiType):
    # imgId = 'aaaaa.peg'
    json_data = {"external_id": f"{external_id}"}
    time.sleep(random.randint(1,3))
    # {'external_id': 'YntB_ZeqRq2l_aVf2gWDCZl4oBttQzDvhj9cXafWcF8'}
    # {'external_id': 'Hpk0GozjACb3mtHeAaAMb0r9pcJGbzF317I_Ux_ALOA'}
    # {'external_id': '9ZSDyg3OuPbFgDqGwy3RpsXqJblE4S1fKA_oU3yvfTM'}
    # {'external_id': '7yDt2WH6Y_OpaAV4GsxKcY5xIQ8QT5M0kgpDQ6VAflI'}
    url = 'https://beta.character.ai/chat/character/'   #设置页面
    # response = requests.get(url=url, proxies=proxy,impersonate=random.choice(TLSAll),headers=headers,json=json_data)
    response = HttpUtil.getPost(url,headers,json_data)
    if response.json().get('characterAI'):
        tags = aiType
        # tags = 'Featured'
        result = response.json().get('characterAI')
        title = result.get('title')
        character_name = ''.join(result.get('name'))
        greeting = result.get('greeting')
        short_description = result.get('title') #有时空  有时是title
        if short_description == None:short_description = ''
        long_description  = result.get('description')
        sample_dialog = result.get('definition')
        if sample_dialog == None:sample_dialog = ''
        categories = result.get('categories')
        character_visibility = result.get('visibility')
        if character_visibility == None:character_visibility = ''
        definition_visibility = result.get('visibility')
        identifier = result.get('identifier')
        avatar_file_name = result.get('avatar_file_name')
        definition = result.get('definition')
        user_username = result.get('user__username')
        participant_name = result.get('participant__name')
        print(participant_name)
        participant_user_username = result.get('participant__user__username')
        img_url = f'https://characterai.io/i/400/static/avatars/{imgId}'
        ImgFileId = ''.join(re.findall('avatars.*/(.*)', img_url, re.S)).strip()
        if '.' in ImgFileId:
            response = requests.get(url=img_url, headers=headers, proxies=proxy,verify=False, timeout=18)
            with open(r"E:\Img\characterImg/{}".format(ImgFileId),"wb") as f:  # 下载封面
                f.write(response.content)
        external_id = result.get('external_id')
        data_dict = dict(
            title=escape_string(str(title)),
            character_name=escape_string(str(character_name)),
            greeting=escape_string(str(greeting)),
            short_description=escape_string(str(short_description)),
            long_description=escape_string(str(long_description)),
            sample_dialog=escape_string(str(sample_dialog)),
            categories=escape_string(str(categories)),
            tags=escape_string(str(tags)),
            character_visibility=character_visibility,
            definition_visibility=escape_string(str(definition_visibility)),
            identifier=escape_string(str(identifier)),
            avatar_file_name=escape_string(str(avatar_file_name)),
            definition=escape_string(str(definition)),
            user_username=escape_string(str(user_username)),
            participant_name=escape_string(str(participant_name)),
            participant_user_username=escape_string(str(participant_user_username)),
            img_url=img_url,
            external_id=external_id
        )
        # print(result)
        print(f'正在插入第{1}条')
        # MySqlSSH().fetch_all('characterAi', data_dict, 'external_id',external_id)
if __name__ == '__main__':
    initialSpider()