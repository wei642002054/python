import random
import time
import json
import requests
import urllib3
from fake_useragent import UserAgent
from http.cookiejar import CookieJar
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
def getCookie():
    url = 'https://www.zhihu.com/signin?next=%2F'
    ua = UserAgent()
    header = {
                'User-Agent': ua.random,
            }
    respon = requests.get(url=url,headers=header,timeout=8,verify=False)
    cookiejar = respon.cookies
    cookies = requests.utils.dict_from_cookiejar(cookiejar)
    cookie = []
    cookie.append('d_c0=ADBSw1ulgxePTjzMPBJJHZQQO146eRLCqQA=|1696751600;')
    for item in cookies:
        cookie.append(item+'='+cookies[item]+';')
    return ''.join(cookie)

