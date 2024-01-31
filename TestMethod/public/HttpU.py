#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author      :jerry
# @File        : __init阿__.py.py
# @Software    : PyCharm
# @description : redis连接池
import os,re
import ssl
import time
import uuid
import requests
from requests.adapters import HTTPAdapter
import urllib3
import random
from TestMethod.db.linkMariaDB import MySqlSSH
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context
TLSAll = ["edge99","edge101","chrome99","chrome100","chrome101","chrome104","chrome107","chrome110","chrome99_android","safari15_3","safari15_5"]
from requests_toolbelt import SSLAdapter
adapter = SSLAdapter('TLSv1')
s = requests.Session()
s.mount('https://', adapter)
class HttpUtil(object):
    proxies = {
        'http': 'http://HNY2FYRVVLF55Y1D:A85903D56A49DD73@http-dyn.abuyun.com:9020',
        'https': 'http://HNY2FYRVVLF55Y1D:A85903D56A49DD73@http-dyn.abuyun.com:9020'
    }
    proxy11={
            "https": "127.0.0.1:7890",
            "http": "127.0.0.1:7890"
    }
    #http://192.168.0.137:5001/V0/get-ip/?t=2&n=1
    #http://192.168.0.122:5001/V0/get-ip/
    session = None
    # IpUrl = 'http://127.0.0.1:51601/proxy/lru/?size=2'
    # IP = requests.get(url=IpUrl).json()
    # proxies = {
    # 'http': 'http://{}'.format(IP[0]),
    # # 'https':'https://{}'.format(IP[-1]),
    # }
    @classmethod  # 静态方法是由类调用的
    def init(cls):
        if not cls.session:
            req_sess = requests.Session()
            req_sess.mount('http://', HTTPAdapter(max_retries=10))
            req_sess.mount('https://', HTTPAdapter(max_retries=10))
            cls.session = req_sess
        return cls.session

    @staticmethod
    def get(url, header, ok_str, timeout=24, retry_num=6):
        HttpUtil.init()
        for i in range(retry_num):
            try:
                resp = HttpUtil.session.get(url=url, headers=header, timeout=timeout,verify=False)# proxies=HttpUtil.proxies,
                if resp.status_code == 200:
                    if ok_str in resp.text:
                        return resp
            except Exception as e:
                print('请求异常{0}'.format(str(e)))
        return None

    def createDir(path):  # 创建文件夹
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            else:
                print('该文件夹已存在')

        except:
            print('创建文件失败！')
    @staticmethod  #普通图片下载
    def gain(url, header, timeout=32, retry_num=8):
        for i in range(retry_num):
            try:
                response = requests.get(url=url, headers=header,proxies=HttpUtil.proxy11,stream=True, timeout=timeout,verify=False)
                if response.status_code == 200:
                    return response
                if response.status_code == 429:
                    print('限制访问频率请等待8分钟')
                    time.sleep(480)
            except Exception as e:
                print('请求异常{0}'.format(str(e)))
        return None
    @staticmethod  #浏览器指纹验证
    def getPost(url, header,payload, timeout=32, retry_num=8):
        from curl_cffi import requests
        for i in range(retry_num):
            try:
                response = requests.get(url=url, headers=header,json=payload,proxies=HttpUtil.proxy11,impersonate=random.choice(TLSAll), timeout=timeout,verify=False)
                # print(url, header,payload,response.status_code)
                if response.status_code == 200:
                    return response
            except Exception as e:
                print('请求异常{0}'.format(str(e)))
        return None
    @staticmethod  #TLS指纹验证
    def Rget(url, header, timeout=32, retry_num=8):
        from curl_cffi import requests
        for i in range(retry_num):
            try:
                response = requests.get(url=url, headers=header,proxies=HttpUtil.proxy11,impersonate=random.choice(TLSAll), timeout=timeout,verify=False)
                # print(response.status_code)
                if response.status_code == 200:
                    return response
            except Exception as e:
                print('请求异常{0}'.format(str(e)))
        return None

    @staticmethod
    def JsonGet(url, header, ok_str, timeout=24, retry_num=8):
        from curl_cffi import requests
        for i in range(retry_num):
            try:
                resp = requests.get(url=url, headers=header,proxies=HttpUtil.proxy11,impersonate=random.choice(TLSAll), timeout=timeout,verify=False)
                if resp.status_code == 200:
                    if ok_str in resp.json():
                        return resp
            except Exception as e:
                print('请求异常{0}'.format(str(e)))
        return None
# proxy= {
#         "https": "127.0.0.1:7890",
#         "http": "127.0.0.1:7890"
#             }
# url = 'https://tq.lunaproxy.com/getflowip?neek=1051374&num=50&type=2&sep=1&regions=all&ip_si=1&level=1&sb='
# resp = requests.get(url,proxies=proxy)
# info = resp.json()['data']
# for i in info:
#     pp = i['ip']+':'+i['port']
#     data = dict(ip=pp)
#     MySqlSSH().insertDirect('roleIpPool',data)
    @staticmethod  #普通图片下载
    def ggg(url, header, timeout=15, retry_num=2):
        for i in range(retry_num):
            try:
                response = requests.get(url=url, headers=header,proxies=HttpUtil.proxy11,stream=True, timeout=timeout,verify=False)
                if response.status_code == 200:
                    return response
            except Exception as e:
                print('请求异常{0}'.format(str(e)))
        return None