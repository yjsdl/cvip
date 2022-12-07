# -*- coding: utf-8 -*-
# @Time    : 2021/12/13 14:23
# @Author  : ZhaoXiangPeng
# @File    : 详情页test1.py

import re
import requests

url = "http://qikan.cqvip.com/Qikan/Article/Detail?id=670668565"

headers = {
    'Proxy-Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
cookies = {}

session = requests.session()
response = session.request("GET", url, headers=headers)
print(response)
resp_cookie = response.cookies
for k in resp_cookie.keys():
    cookies[k] = resp_cookie.get(k)
print(cookies)
meta = re.findall(r'<meta content="(.*?)"><!--\[if lt IE 9]>', response.text)
meta = meta[0]
print(meta)

response = session.request("GET", url, headers=headers, cookies=cookies)
print(response)
