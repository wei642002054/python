# input = 'avatar_url_template'
# out_str = re.sub(r'[A-Z]', lambda pat: '_'+pat.group().lower(), input)
# print(out_str)
import requests
import time,re
import logging
import json   #专栏·页面
import jsonpath
import hashlib
import urllib.parse   #is_end=true  获取完  false没获取完
import execjs
from _md5 import md5
from lxml import etree
from requests.adapters import HTTPAdapter
import base64
from TestMethod.public.HttpU import HttpUtil
from TestMethod.public.initLog import init_log_config
from TestMethod.zhihuDemo.X_96_V3 import *
from TestMethod.zhihuDemo.ZhiHCookieJar import getCookie
url_token = 'zhi-hu-lu-xing-96'  #博主
url_type = 'articles'
proxy = HttpUtil.proxy11
include = 'data%5B*%5D.comment_count%2Csuggest_edit%2Cis_normal%2Cthumbnail_extra_info%2Cthumbnail%2Ccan_comment%2Ccomment_permission%2Cadmin_closed_comment%2Ccontent%2Cvoteup_count%2Ccreated%2Cupdated%2Cupvoted_followees%2Cvoting%2Creview_info%2Creaction_instruction%2Cis_labeled%2Clabel_info%3Bdata%5B*%5D.vessay_info%3Bdata%5B*%5D.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B*%5D.author.vip_info%3B'
zst_81 = '3_2.0aR_sn77yn6O92wOB8hPZnQr0EMYxc4f18wNBUgpTQ6nxERFZGXY0-4Lm-h3_tufIwJS8gcxTgJS_AuPZNcXCTwxI78YxEM20s4PGDwN8gGcYAupMWufIeQuK7AFpS6O1vukyQ_R0rRnsyukMGvxBEqeCiRnxEL2ZZrxmDucmqhPXnXFMTAoTF6RhRuLPFRcYMqpB3wHGNhVmOGeLAwYmVBLMZD3MggNYhGx9zg9CbCtYqqo9KBx16rSTvMV_gbNBMhxKeRHBJ0ompqg0xBpOXJ31kBFMSHNYXrSYwqUfFBL9CwH_0gC8jb3_VJOYpqHGpGYy1JOfJRpY_UNCJwY_t9HOSQxMXwYMGwwKiwe_YGN9VqfzGu28Wh3BBUVfLBxydCe9nrU9SggmuUSmYbOqDDwOAcHpbiHC7gLC_UxLUDCpaqeCWwc9ubVmoRts3gXK1ugYDbH0kXe98DwqQDw96MLL9cn_QXHLwBgC'
def xzse96_spider(url_token,url_type,include,count):
    refer = '/api/v4/members/{}/{}?include={}&offset=0&limit=20&sort_by=created'.format(url_token, url_type, include, count)
    s = "+".join(['101_3_3.0',refer,'ADBSw1ulgxePTjzMPBJJHZQQO146eRLCqQA=|1696751600',zst_81])
    print(s)
    sMd5 = md5(s.encode()).hexdigest()
    print(sMd5)
    # node = execjs.get()
    # print(sMd5)
    # # file_js = r'D:\Python123\CsvCode\zhihu_v1.1\zhihu\task\test\textx.js'
    # file_js = 'D:\Python123\CodePath\code\signature.js'
    # ctx = node.compile(open(file_js,encoding='utf-8').read())
    # funcName = 'get_sig("{}")'.format(sMd5)
    # # funcName = 'b("{}")'.format(sMd5)
    # xzse96 = ctx.eval(funcName)
    x_96_endata = x_zse_96_V3.b64encode(bytes(sMd5,encoding = "utf-8"))
    # print(x_96_endata)
    # print('vPcVArL6bdVYk2MHbFlqQj1prbAhuILuWy2cRAWbWknnu0Wm=8o6Kt9a0UVS1js7')
    y = x_zse_96_V3.b64decode(x_96_endata)
    print(y,type(y))
    # return xzse96
    # y = xzse96
    xzse96 = '2.0_' + x_96_endata
    # xzse96 = "2.0_" + y
    print(xzse96)
    return xzse96
def result_spider():
    count = 0
    try:
        xzse96 = xzse96_spider(url_token,url_type,include,count*20)
        headers = {
            'cookie': getCookie(),
            #'cookie': 'd_c0=ADBSw1ulgxePTjzMPBJJHZQQO146eRLCqQA=|1696751600;_xsrf=5bca0bd5-9005-4952-bf26-8085864ce887;_zap=2f68874e-1522-48db-94a4-e5ff37340756;KLBRSID=cdfcc1d45d024a211bb7144f66bda2cf|1697449708|1697449708;',
            'X-Zse-93': '101_3_3.0',
            'X-Zse-96': xzse96, #
            # 'x-zse-96': '2.0_3m9oZk+B9e0C7WDUyvycmJ9ltZcx7o9cmHgkOmsDa6uJmPV66CztGYq==xvhpGcu',
            # 'x-udid':'APCQNnC19xOPTiOOre_CS_sVTcMyFChLKdM=',
            'X-Zst-81':zst_81,
            # 'x-zst-81':'3_2.0VhnTj77m-qofgh3TxTnq2_Qq2LYuDhV80wSL7iUZQ6nxE7t0m4fBJCHMiqHPD4S1hCS974e1DrNPAQLYlUefii7q26fp2L2ZKgSfnveCgrNOQwXTt_Fq6DQye8t9DGwT9RFZQAuTLbHP2GomybO1VhRTQ6kp-XxmxgNK-GNTjTkxkhkKh0PhHix_F0nOjhN1qgNBpcwqeBtOoeO8uugG0ucLtBxxyqNfGhLKCcx1xJx8UDSfZ9L1FH_z68CBuG3YKDCYk8OYJrXm0DSGMqCBWgeGQAOpwBg1BhLB20XG2BpffwXMmGpqDq981cxm1hY83cO9svoCcRwVxq2YnDoB8UVyCre_LCcB84wGWJOCwBXs',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        }
        # url = 'https://www.zhihu.com/api/v4/comment_v5/articles/385070361/root_comment?order_by=score&limit=20&offset='
        # "https://www.zhihu.com/api/v4/comment_v5/articles/384498141/root_comment?limit=20&offset=5_10380841520_0&order_by=score"
        requests.packages.urllib3.disable_warnings()
        print('正在获取第{}页'.format(count + 1))
        # url = 'https://www.zhihu.com/api/v4/members/michelleqx/questions?include=data%5B*%5D.created%2Canswer_count%2Cfollower_count%2Cauthor%2Cadmin_closed_comment&offset=0&limit=20'
        url = 'https://www.zhihu.com/api/v4/members/zhi-hu-lu-xing-96/articles?include=data%5B*%5D.comment_count%2Csuggest_edit%2Cis_normal%2Cthumbnail_extra_info%2Cthumbnail%2Ccan_comment%2Ccomment_permission%2Cadmin_closed_comment%2Ccontent%2Cvoteup_count%2Ccreated%2Cupdated%2Cupvoted_followees%2Cvoting%2Creview_info%2Creaction_instruction%2Cis_labeled%2Clabel_info%3Bdata%5B*%5D.vessay_info%3Bdata%5B*%5D.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B*%5D.author.vip_info%3B&offset=0&limit=20&sort_by=created'
        # url = 'https://www.zhihu.com/api/v4/comment_v5/articles/570151071/root_comment?order_by=score&limit=20&offset='
        response = requests.get(url=url,headers=headers, timeout=8, verify=False)
        print(response.status_code,response.json())
    except:
        init_log_config()
        logging.info("报错信息: [%s], || URl链接:%s" % ('loser', 'url'))


result_spider()
