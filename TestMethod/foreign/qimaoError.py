import requests
import os

proxy= {
    "https": "127.0.0.1:7890",
    "http": "127.0.0.1:7890"
}
import ssl
import re
import requests
# url = 'https://api-bc.wtzw.com/api/v3/recommend/high-score?gender=2&page_no=2&read_preference=0&book_privacy=1&sign=0696f830a3b4ec500e5a4810680a853d'
# url = 'https://api-bc.wtzw.com/api/v5/category/get-list?book_preference=2&need_filters=0&over=-99&words=-99&need_supplement=0&gender=2&read_preference=0&category_type=2&from=0&category_id=772&sort=1&page=10&sign=7e131f48ee4443fcb01af4f0f46c9183'
# url = 'https://api-bc.wtzw.com/api/v5/category/get-list?book_preference=2&need_filters=0&over=-99&words=-99&need_supplement=0&gender=2&read_preference=0&category_type=2&from=0&category_id=772&sort=1&page=5&sign=3f1454d7bbaf8ac7d9e873363596b412'
# url = 'https://api-bc.wtzw.com/api/v5/category/get-list?book_preference=1&need_filters=0&over=-99&words=-99&need_supplement=0&gender=2&read_preference=0&category_type=2&from=0&category_id=717&sort=1&page=2&sign=2d222b616ed0a309b81a567261b3b21b'
url = 'https://api-bc.wtzw.com/api/v5/category/get-list?book_preference=1&need_filters=1&over=-99&words=-99&need_supplement=&gender=2&read_preference=0&category_type=2&from=0&category_id=589&sort=-99&page=1&sign=f4675fb4ef243b1dd1d51a92afe4856e'
# url = 'https://api-bc.wtzw.com/api/v5/category/get-list?book_preference=1&need_filters=0&over=-99&words=-99&need_supplement=0&gender=2&read_preference=0&category_type=2&from=0&category_id=730&sort=1&page=2&sign=a5462bfe5da449152deba0f3287ca6a0'
# url = 'https://api-bc.wtzw.com/api/v5/category/get-list?book_preference=1&need_filters=0&over=-99&words=-99&need_supplement=0&gender=2&read_preference=0&category_type=2&from=0&category_id=730&sort=1&page=2&sign=27109f10ed3a1b3e856227362746cf07'
ssl._create_unverified_context()
# url = 'https://api-ks.wtzw.com/api/v1/chapter/chapter-list?chapter_ver=0&id=122783&sign=7461c7563ade0220a3e73184201b5754'  #总章节 各节count
requests.packages.urllib3.disable_warnings()
# url = 'https://api-bc.wtzw.com/api/v4/book/detail?id=149774&imei_ip=1875352649&teeny_mode=0&read_preference=0&sign=6b3ae9734606521a9d23f5e82d530c4a'
header = {
    'Set-Cookie': 'acw_tc=2760779e16492367999763592eb8e0a8579671c0258082980d49a73b612d80;path=/;HttpOnly;Max-Age=1800',
    'qm-params': 'cLGEByHQmqU2m3HWHTgUNhOUNeKENhgnNegLA3HjHzUx4LHWHT9rAT9wATHEATKYA-oyATfMH5w5uCR1paHWHT9wgI9wgI9wthHMpT4Qgy4lNLMwgI9wth9wgI9wpqfL4Tp5g3HjHzNjmqR7uaU1paHWHTfY4qkTAI-rNeG5NTgwgTH5taGD4q2-HTZ5H5w5u_GUOEk2paU1paHWH-kRtf2ZOqnyOUGhO0o-p0usO2kiA0-eBeoI30oyqoRVfEOEgRGyRCkhRlxr4-Rmc2RjhSukRUGvfTsycRpoBekhR0YlhRRA3RoRq22qREsfp_1TcygLmI05taG-pCp14lfQmqF5A5HLgIHLgIFwNT0UNh9eNhsz4T4Ygl0YNlgw4e4wpIFLpyfM4lfw4eFnAIuTglgegIs2pqHM4qHwpIHYgeR-g3HjHz2Qpq-5A5HeNhfENhOrNefeghOegT-5taG5Ozo7paHWH-JFf0d5taGEByHQuq2-HTZ5gefUNefEAIOUge0EgeHYH5w5OE2etCp2O5HWHTf7g3rnH5w5BqJ-pqw5A5G8fos8HoHng3sFB_ReHSM=',
    # 'qm-params':'cLGEByHQmqU2m3HWHTgUNhOUNeKENhgnNegLA3HjHzUx4LHWHT9rAT9wATHEATKYA-oyATfMH5w5uCR1paHWHT9wgI9wgI9wthHMpT4Qgy4lNLMwgI9wth9wgI9wpqfL4Tp5g3HjHzNjmqR7uaU1paHWHTfY4qkTAI-rNeG5NTgwgTH5taGD4q2-HTZ5H5w5u_GUOEk2paU1paHWH-kRtf2ZOqnyOUGhO0o-p0usO2kiA0-eBeoI30oyqoRVfEOEgRGyRCkhRlxr4-Rmc2RjhSukRUGvfTsycRpoBekhR0YlhRRA3RoRq22qREsfp_1TcygLmI05taG-pCp14lfQmqF5A5HLgIHLgIgnNe0Ugh9nNlfngIx5ph-eNy4M4lk2Ny0nNqFrgIsxpTOYpTxz4hxTgI0UgIKMghNxgqFMgh9wpaHjHz2Qpq-5A5HeNhfENhOrNefeghOegT-5taG5Ozo7paHWH-JFf0d5taGEByHQuq2-HTZ5gefUNefEAIOUge0EgeHYH5w5OE2etCp2O5HWHTf7g3rnH5w5BqJ-pqw5A5G8fos8HoHng3sFB_ReHSM=',
    # 'sign':'9da722ef44e177bef50b547f3f7a6ef6',
    'sign': '4a18cdb878d5ed3b67d5b28bdb103d3d',
    'User-Agent': 'webviewversion/60100',
    'app-version': '60100',
    'platform': 'android',
    'reg': '',
    'AUTHORIZATION': '',
    'is-white': '1',
    'application-id': 'com.kmxs.reader',
    'net-env': '1',
    'channel': 'qm-wy1yd084_wm'
}

# response = requests.get(url=url,proxies=proxy,headers=header,verify=False)
# print(response.json())
#网页
urlw = 'https://www.qimao.com/shuku/149774/'
# url = "https://www.qimao.com/shuku/a-a-a-a-a-a-a-click-1/"
def get_hexxor(s1, _0x4e08d8):
    _0x5a5d3b = ''

    for i in range(len(s1)):
        if i % 2 != 0: continue
        _0x401af1 = int(s1[i: i+2], 16)
        _0x105f59 = int(_0x4e08d8[i: i+2], 16)
        _0x189e2c_10 = (_0x401af1 ^ _0x105f59)
        print(_0x401af1,'aaaaaa',_0x189e2c_10,_0x105f59)
        _0x189e2c = hex(_0x189e2c_10)[2:]
        if len(_0x189e2c) == 1:
            _0x189e2c = '0' + _0x189e2c
        _0x5a5d3b += _0x189e2c
    return _0x5a5d3b


def get_unsbox(arg1):
    _0x4b082b = [0xf, 0x23, 0x1d, 0x18, 0x21, 0x10, 0x1, 0x26, 0xa, 0x9, 0x13, 0x1f, 0x28, 0x1b, 0x16, 0x17, 0x19, 0xd,
                 0x6, 0xb, 0x27, 0x12, 0x14, 0x8, 0xe, 0x15, 0x20, 0x1a, 0x2, 0x1e, 0x7, 0x4, 0x11, 0x5, 0x3, 0x1c,
                 0x22, 0x25, 0xc, 0x24]
    _0x4da0dc = []
    _0x12605e = ''
    for i in _0x4b082b:
        _0x4da0dc.append(arg1[i-1])
    _0x12605e = "".join(_0x4da0dc)
    return _0x12605e


# 第一次请求获取js代码
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"}

r = requests.get(urlw,proxies=proxy, headers=headers)
print(r.text)
# 重js中匹配出 arg1
arg1 = re.findall("arg1=\'(.*?)\'", r.text)[0]

# 参数生成
s1 = get_unsbox(arg1)
_0x4e08d8 = "3000176000856006061501533003690027800375"
_0x12605e = get_hexxor(s1, _0x4e08d8)

# print(s1, _0x12605e)
# 二次请求携带cookie 获取html文件
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
           "cookie": "acw_sc__v2=%s" % _0x12605e}
#解密返回值
r = requests.get(urlw,proxies=proxy, headers=headers)
# print(r.text)
# 没解密返回值
resp = requests.get(url=urlw,proxies=proxy,verify=False)
resp.encoding = resp.apparent_encoding
print(resp.text)