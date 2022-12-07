# -*- coding: utf-8 -*-
# @Time    : 2022/3/4 8:51
# @Author  : ZhaoXiangPeng
# @File    : rs5_encrypt.py
"""
生成一个cookie必须有 meta, js
非列表页的200有meta和js
ts必须与meta绑定
1. 173cookie
    只需要412的meta和js
2. 279cookie
    需要YWTU, 但是200的没有这个参数, 那么需要固定这个参数
"""

import re
import random
import subprocess
import functools

import requests

subprocess.Popen = functools.partial(subprocess.Popen, encoding='utf-8')
import execjs
from ReSpider.utils.tools import str2base64
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class RS5Encrypt:
    YWTU_LIST = []
    META_LIST = []
    CTX = {
        '173': [],
        '279': []
    }
    LOOP = []
    with open('../js/main.js', encoding='utf-8') as fp:
        all_js = fp.read()
    with open('../js/main2.js', encoding='utf-8') as fp:
        all_js2 = fp.read()

    def __init__(self, ctx_size: int = 1):
        self.CTX_SIZE = ctx_size

    def register_200(self, meta_str: str = None, js_code: str = None, ywtu_str: str = None, cookies: dict = None):
        ctx = None
        if self.CTX['279'].__len__() == self.CTX_SIZE:
            self.CTX['279'].pop()
        if self.CTX['279'].__len__() <= self.CTX_SIZE:
            eval_row = re.findall(r'_\$\S{2}=_\$\S{2}\[_\$\S{2}\[13]]\(_\$\S{2},_\$\S{2}\)', js_code)[0]
            eval_js_name = eval_row[-5:-1]  # eval代码变量名
            # 拿到window.$_ts
            hook_js = js_code.replace(eval_row, f'ret="zaoxg";eval_js_content={eval_js_name};ts=window.$_ts;')
            excjs = self.all_js2.replace('indexjsyeah', hook_js)
            ctx = execjs.compile(excjs)  # 锁定meta和ts
            self.CTX['279'].append({
                'CTX': ctx,
                'META': meta_str,
                'COOKIE': cookies
            })
        else:
            return self.get279_cookie()
        try:
            if ywtu_str and meta_str:
                return ctx.call('rs5Encrypt', meta_str, ywtu_str)
            else:
                return ctx.call('rs5Encrypt', meta_str, random.choice(self.YWTU_LIST))
        except execjs._exceptions.ProgramError as execjs_error:
            logger.warning('%s' % execjs_error)

    def get173_cookie(self, meta_str: str, js_code: str):
        """
        需要保存 YWTU
        :param meta_str:
        :param js_code:
        :return:
        """
        eval_row = re.findall(r'_\$\S{2}=_\$\S{2}\[_\$\S{2}\[13]]\(_\$\S{2},_\$\S{2}\)', js_code)[0]  # 4代是 ret
        eval_js_name = eval_row[-5:-1]  # eval后的结果
        # 拿到window.$_ts
        hook_js = js_code.replace(eval_row, f'ret="zaoxg";eval_js_content={eval_js_name};ts=window.$_ts;')
        excjs = self.all_js.replace('indexjsyeah', hook_js)
        ctx = execjs.compile(excjs)
        exec_res = ctx.call('rs5Encrypt', meta_str)
        self.YWTU_LIST.append(exec_res['YWTU'])
        return exec_res

    def get279_cookie(self):
        this_ctx = self.CTX['279'].pop(0)
        call_res: dict = this_ctx['CTX'].call('rs5Encrypt', this_ctx['META'], random.choice(self.YWTU_LIST))
        call_res.update({'COOKIE': this_ctx['COOKIE']})
        self.CTX['279'].append(this_ctx)
        return call_res

    def get_param_from_resp(self, meta, js):
        eval_row = re.findall(r'_\$\S{2}=_\$\S{2}\[_\$\S{2}\[13]]\(_\$\S{2},_\$\S{2}\)', js)[0]  # 4代是 ret
        eval_js_name = eval_row[-5:-1]  # eval后的结果
        # 拿到window.$_ts
        # hook_js = js_code.replace(eval_row, f'ret="zaoxg";eval_js_content={eval_js_name};ts=window.$_ts;')
        ret4 = eval_row[:4]
        hook_js = js.replace(eval_row,
                             f'{ret4}=undefined;eval_js_content={eval_js_name};window_ts=window.$_ts;break;;;;;')  # window.$_ts=undefined;$_ts=undefined
        js_base64 = str2base64(hook_js)
        # print('python call: ', self.rs5.get173_cookie(meta, js).get('ARR4'))
        resp = requests.post('http://127.0.0.1:9001/ruishu/5/cqvip',
                             data={'meta': meta, 'js': js_base64})
        exec_res = resp.json()
        print('nodejs call: ', exec_res.get('ARR4'))
        # pprint(exec_res)
        cookie = exec_res.get('COOKIE_T')
        # print(cookie)
        # cookies.update({'GW1gelwM5YZuT': cookie})
        print('cookies 长度是: %s' % cookie.__len__())
        return exec_res

RS5Encrypt(1)