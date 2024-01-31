# -*- encoding: utf-8 -*-
import os,re
import ssl
import requests
from requests.adapters import HTTPAdapter
import urllib3
import random

from TestMethod.db.linkMariaDB import MySqlSSH

urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context
from TestMethod.foreign.rolePlayForum.AmericaDataBase import AmericaInsertData
TLSAll = ["edge99","edge101","chrome99","chrome100","chrome101","chrome104","chrome107","chrome110","chrome99_android","safari15_3","safari15_5"]
s = requests.session()
s.keep_alive = False
def proxys():
    # proxy_pool = AmericaInsertData().searchIP() #35美国
    proxy_pool = MySqlSSH().searchIP() #01
    if len(proxy_pool) < 1:proxy_pool = ['pr.dq03qqo6.lunaproxy.net:12233']
    IpEntry = 'http://{}:{}@{}'.format("user-lu9918425", "Nv2g2jEnTUv3McF", random.choice(proxy_pool))
    proxy = {
        'http': IpEntry,
        'https': IpEntry,
    }
    return proxy
class HttpProxy(object):
    entry = 'http://{}:{}@pr.dq03qqo6.lunaproxy.net:12233'.format("user-lu9918425", "Nv2g2jEnTUv3McF")
    proxy = {
        'http': entry,
        'https': entry,
    }
    @staticmethod
    def get(url, header, ok_str, timeout=24, retry_num=6):
        sess = requests.Session()
        sess.mount('http://', HTTPAdapter(max_retries=3))
        sess.mount('https://', HTTPAdapter(max_retries=3))
        sess.keep_alive = False # 关闭多余连
        for i in range(retry_num):
            try:
                print(proxys(),'*************************-------((((((((((((((')
                resp = s.get(url=url, headers=header,proxies=proxys(), timeout=timeout,verify=False)
                resp.close()
                requests.adapters.DEFAULT_RETRIES = 5
                if resp.status_code == 200:
                    if ok_str in resp.text:
                        return resp
            except Exception as e:
                print('请求异常{0}'.format(str(e)))
        return None
    @staticmethod  #TLS指纹验证
    def Rget(url, header, timeout=32, retry_num=8):
        from curl_cffi import requests
        for i in range(retry_num):
            try:
                response = requests.get(url=url, headers=header,proxies=HttpProxy().proxy,impersonate=random.choice(TLSAll), timeout=timeout,verify=False)
                if response.status_code == 200:
                    return response
            except Exception as e:
                print('请求异常{0}'.format(str(e)))
        return None