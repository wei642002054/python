"""
------------------------- headers格式化 ---------------------------
@ 从浏览器直接复制的headers格式化,使requests可用

"""

import pprint

chrome_headers = '''

Cookie:sucuri_cloudproxy_uuid_34c0152b9=116119db20cee4878fba8925c27811d9
Referer:https://www.simplyscripts.com/movie-screenplays.html
Sec-Ch-Ua:"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"
Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36

'''
a = '6111002976816202300106'
print(a[6])
request_headers = {}
for i in chrome_headers.split('\n'):
    data_list = i.strip().split(': ')
    for data in data_list:
        if data_list[0] != '':
            request_headers[data_list[0]] = data_list[1]
pprint.pprint(request_headers)
