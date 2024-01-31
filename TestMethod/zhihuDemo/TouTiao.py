import requests
import urllib3
import ssl
import os
import re
import json
from lxml import etree
import random
import execjs
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter
from TestMethod.public.HttpU import HttpUtil
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
paylode = {
    'channel_id': '3189398996',
    'min_behot_time': '0',
    'offset': '0',
    'refresh_count': '1',
    'category': 'pc_profile_channel',
    'client_extra_params': '{"short_video_item":"filter"}',
     'aid': '24',
     'app_name': 'toutiao_web',
    '_signature': '_02B4Z6wo00101wd9hWAAAIDDh39.IwZvnq8HWYHAAKT3rKqNpdKNHnjm3S-3dYgT9KqODBoZOtoZY2ubv6fJoLMAZuoe3JC7zH98-E45v71bQ8zieM3XIhpKxOLjeuknlKbk-Iql5B2Zoatl72',
}
ua = UserAgent()
header = {
    'Sec-Ch-Ua-Platform':'"Windows"',
    'Sec-Fetch-Dest':'empty',
    'Sec-Fetch-Mode':'cors',
    'Sec-Fetch-Site':'same-origin',
    'Referer':'https://www.toutiao.com/',
    # 'Cookie':'msToken=B3snoC7ZGD0BdfOi_5a672VitS4jqn3S8zjpoTWxBg8DREfwAWjXc2af4XOcQ-wsgScpt8PsaaE-TlMY8r7NWe6XsaYpu2WvtBTppg_t; __ac_signature=_02B4Z6wo00f01MrAk.AAAIDASsJpsRbaHNTK4JdAAFeG5f; tt_webid=7291604674959017511; ttcid=35f4e3a82769423abbfcacfc888bb0b323; s_v_web_id=verify_lnx04fb4_bSCMfTAr_BhAl_4Zjy_AiAN_RQZipuqnw4vV; local_city_cache=%E5%8C%97%E4%BA%AC; csrftoken=0d74b1c43bb028ef4094c52ad79fd1fc; _ga=GA1.1.798053722.1697711177; _ga_QEHZPBE5HH=GS1.1.1697784073.4.1.1697785047.0.0.0; ttwid=1%7CySp-YBy-NWCbvzcI15SmJmjRIA4MCZjoDYJd6YjW028%7C1697785049%7Cf04eb88c6ae4a0f9eb86742d0635c06ad81315cef254084d0d728f55e8d91034; tt_scid=ygFCGJX6xPcscCkMXYDnRHeWlZ7o8Vrqtx9TWWtjz2fOUdv6Lc21Zwl.1sh9LJJ979b7',
    'User-Agent': ua.random,
}
proxy_pool = HttpUtil.proxy11
# proxy_pool = None
uId= 'https://www.toutiao.com/api/pc/list/feed?channel_id=3189398996&min_behot_time=0&offset=0&refresh_count=1&category=pc_profile_channel&client_extra_params=%7B%22short_video_item%22:%22filter%22%7D&aid=24&app_name=toutiao_web'
o =  {
    'url':uId
}
JsPath = r'E:\PythonFile\PyCode\TestMethod\ExJsFile\TTSing.js'
sign = execjs.compile(open(JsPath,'r',encoding='utf-8').read()).call('getSign',o)
url = uId+'&_signature='+sign
response = requests.get(url=url,headers=header,proxies=proxy_pool,timeout=8,verify=False)
print(response.text)