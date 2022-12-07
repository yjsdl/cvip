# -*- coding: utf-8 -*-
# @Time    : 2022/3/3 10:37
# @Author  : ZhaoXiangPeng
# @File    : middleware.py

import re
import asyncio
import ReSpider
from ReSpider.middlewares import BaseMiddleware
from ReSpider.middlewares.proxy import ProxyMiddleware
import ReSpider.setting as setting
from cqVIP.util.rs5_encrypt import RS5Encrypt


class Rs5CookieMiddleware(BaseMiddleware):
    rs5 = None

    def open_spider(self, spider=None, **kwargs):
        self.rs5 = RS5Encrypt(setting.TASK_LIMIT * 2)

    async def process_request(self, request):
        if request.method == 'POST':
            try:
                cookie_res = self.rs5.get279_cookie()
            except Exception as e:
                req = ReSpider.Request(
                    url='http://qikan.cqvip.com/')
                resp = await req()
                cookies = resp.cookiejar
                meta, js = self.get173(resp)
                eval_res = self.rs5.get173_cookie(meta, js)
                cookie_t = eval_res.get('COOKIE_T')
                cookies.update({'GW1gelwM5YZuT': cookie_t})
            else:
                cookies = cookie_res['COOKIE']
                cookies.update({'GW1gelwM5YZuT': cookie_res['COOKIE_T']})
            request.priority = 0
            request.cookies = cookies
        return request

    async def process_response(self, request, response):
        cookies = response.cookiejar
        if response.status == 412:
            if request.method == 'POST':
                self.logger.info('POST 请求失败')
                self._observer.request_count_fail = 1
                # self.logger.info('重新获取ts')
                await self.reget()
                request.priority = 1
                request.retry_times += 1
                request.do_filter = False
                return request
            meta, js = self.get173(response)
            eval_res = self.rs5.get173_cookie(meta, js)
            cookie_t = eval_res.get('COOKIE_T')
            cookies.update({'GW1gelwM5YZuT': cookie_t})
            # self.logger.debug('cookies 长度是: %s' % cookie_t.__len__())
            request.priority = 0
            request.do_filter = False
            request.cookies = cookies
            request.ywtu = eval_res.get('YWTU')
            return request
        elif response.status != 200:
            self._observer.request_count_fail = 1
            request.do_filter = False
            return request
        else:
            req_cookie = response.request.cookies
            req_cookie.update(cookies)
            meta, js = self.get279(response)
            if meta:
                self.rs5.register_200(meta, js, request.__dict__.get('ywtu'), req_cookie)
        return response

    def get173(self, response):
        meta = response.re_first(r'<meta content="(.*?)"><!--\[if lt IE 9]>')
        # print(meta)
        js: list = re.findall(r'</script><script type="text/javascript" r=\'m\'>(.*?)</script></head>',
                              response.text)  # 首页js
        if js:
            js: str = js[0]
        return meta, js

    def get279(self, response):
        request = response.request
        if request.__dict__.get('ywtu'):
            ywtu = request.ywtu
        meta = response.re_first(r'<meta content="(.*?)"><!--\[if lt IE 9]>')
        js: list = re.findall(r'</script><script type="text/javascript" r=\'m\'>(.*?)</script><script',
                              response.text)
        if js:
            js: str = js[0]
        return meta, js

    async def reget(self):
        req = ReSpider.Request(
            url='http://qikan.cqvip.com/Qikan/Search/Advance?from=index')
        resp = await req()
        cookies = resp.cookiejar
        meta, js = self.get173(resp)
        eval_res = self.rs5.get173_cookie(meta, js)
        cookie_t = eval_res.get('COOKIE_T')
        cookies.update({'GW1gelwM5YZuT': cookie_t})
        req = ReSpider.Request(
            url='http://qikan.cqvip.com/Qikan/Search/Advance?from=index',
            cookies=cookies)
        resp = await req()
        cookies = resp.cookiejar
        req_cookie = resp.request.cookies
        req_cookie.update(cookies)
        meta, js = self.get279(resp)
        if meta and js:
            try:
                self.rs5.register_200(meta, js, None, req_cookie)
            except TypeError as te:
                self.logger.info(te, exc_info=True)
        self.logger.info('重新获取ts成功')


class Rs5CookiePostMiddleware(Rs5CookieMiddleware):
    async def process_request(self, request):
        if request.method == 'POST':
            req = ReSpider.Request(
                url='http://qikan.cqvip.com/Qikan/Search/Advance?from=index')
            resp = await req()
            cookies = resp.cookiejar
            meta, js = self.get173(resp)
            eval_res = self.rs5.get173_cookie(meta, js)
            # eval_res = self.rs5.get_param_from_resp(meta, js)
            cookie_t = eval_res.get('COOKIE_T')
            cookies.update({'GW1gelwM5YZuT': cookie_t})
            request.priority = 0
            request.cookies = cookies
        return request

    async def process_response(self, request, response):
        cookies = response.cookiejar
        if response.status == 412:
            if response.status == 412:
                if request.method == 'POST':
                    self.logger.info('POST 请求失败')
                    self._observer.request_count_fail = 1
                    # self.logger.info('重新获取ts')
                    request.do_filter = False
                    return request
                meta, js = self.get173(response)
                eval_res = self.rs5.get173_cookie(meta, js)
                # eval_res = eval_res = self.rs5.get_param_from_resp(meta, js)
                cookie_t = eval_res.get('COOKIE_T')
                cookies.update({'GW1gelwM5YZuT': cookie_t})
                # self.logger.debug('cookies 长度是: %s' % cookie_t.__len__())
                request.priority = 0
                request.do_filter = False
                request.cookies = cookies
                request.ywtu = eval_res.get('YWTU')
                return request
        elif response.status != 200:
            self._observer.request_count_fail = 1
            request.do_filter = False
            return request
        else:
            return response


class RsProxyMiddleware(ProxyMiddleware):
    proxies = []
    has_ip = True

    def open_spider(self, spider=None, **kwargs):
        import asyncio
        if self.proxies.__len__() < 1:
            asyncio.run(self.get_proxy(num=setting.TASK_LIMIT + 2))

    async def process_request(self, request):
        if self.proxies.__len__() < 1:
            await self.get_proxy()
        try:
            proxy = self.proxies.pop(0)
        except IndexError:
            self.logger.warning('没有可以使用的ip')
        else:
            request.proxy = proxy
        # self.logger.info(request.seen())
        return request

    async def process_response(self, request, response):
        if response.status in {604, 602, 401}:
            self.logger.warning(response.exception)
        elif request.proxy != '':
            self.proxies.append(request.proxy)
        return response

    async def get_proxy(self, num: int = 1):
        lock = asyncio.Lock()
        async with lock:
            num = setting.TASK_LIMIT - self.proxies.__len__()
            req = ReSpider.Request(
                url=f'http://webapi.http.zhimacangku.com/getip?num=5&type=2&pro=&city=0&yys=0&port=1&pack=234261&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=')
            resp = await req()
            resp_json: dict = resp.json()
            self.logger.warning('ip: %s' % resp_json)
            if resp_json.get('code') != 0:
                return
            proxy = [f'http://{proxy.get("ip")}:{proxy.get("port")}' for proxy in resp_json['data']]
            # ip_req = ReSpider.Request(
            #     url='http://httpbin.org/ip',
            #     proxy='http://'+proxy
            # )
            # ip_resp = await ip_req()
            # if ip_resp.json()['origin'] == proxy.split(':')[0]:
            self.proxies += proxy
