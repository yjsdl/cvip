# -*- coding: utf-8 -*-
# @Time    : 2022/03/07 13:20
# @Author  : PC-006
# @File    : reference_by_api.py

import ReSpider
from ReSpider import item
import pandas as pd
# from ReSpider.core.downloader import DownloadHandler
import pymongo

clint = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = clint.data_temp


class ReferenceByApi(ReSpider.Spider):
    saveDB = 'data_weipu_cscd'
    __custom_setting__ = {
        'TASK_LIMIT': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL_CONSOLE': 'INFO',
        'LOG_TO_FILE': True,
        'SCHEDULER': 'ReSpider.extend.redis.scheduler.RedisScheduler',
        'DOWNLOADER_MIDDLEWARES': {
            'cqVIP.middleware.Rs5CookieMiddleware': 5,
            # 'cqVIP.middleware.RsProxyMiddleware': 7
        }
    }
    start_urls = []

    def start_requests(self):
        temp1 = db[self.saveDB].distinct("url")
        print(len(temp1))
        df = pd.read_csv(r'F:\工作数据存储2022\20220421_cssci更新\华中农业大学/华中农业大学2022cscd.csv')
        # df = pd.read_excel(r'F:/工作数据存储2022/20220301_ers数据更新/中国地质大学2021中文发文.xlsx', engine='openpyxl')[:100]  # [150000:]
        df.dropna(subset=['网址'], inplace=True)
        URLS = df['网址'].values.tolist()
        URLS = set(URLS) - set(temp1)
        URLS = list(set(URLS))
        print(len(URLS))
        for url in URLS:
            yield ReSpider.Request(
                url=url,
                do_filter=True,
                retry=True,
                meta={'url': url,
                      'id': url.split('=')[-1]},
                callback=self.parse  # 第一次取cookie
            )

    async def parse(self, response):
        # 引文 被引量解析
        meta = response.meta
        # self.logger.debug(response.xpath('//title/text()').get())
        # print(response.text)
        cookiejar = response.cookies
        # html = etree.HTML(response.content)
        byl = response.xpath('//div[@id="body"]/div/div/div[1]/div[1]/h1/span[@class="cited"]/a/text()').get()
        article_list_nodes = response.xpath(
            '//div[@id="referenceRelate"]/div[@class="relate"]/div[@class="article-list"]/ul[@id="referenceRelateInfo"]/li')
        # byl = byl[0] if byl else 0
        meta.update(byl=byl)
        data_list = item.DataListItem(collection=self.saveDB)
        for article_list_node in article_list_nodes:
            article_ = article_list_node.xpath('.//text()').getall()
            article_ = [a.strip() for a in article_ if a.strip() != '']
            article = ' '.join(article_)
            data = dict(aid=meta.get('id'),
                        url=meta.get('url'),
                        yinwen=article,
                        byl=byl)
            data_list.append(data)
            self.logger.debug(data)
        yield data_list
        # 统计参考文献数量
        literature = response.xpath('//div[@id="referenceRelate"]/div/div[1]/h2/span/text()').getall()
        total = int(literature[0] if literature else 0)
        if total % 10 > 0:
            page = total // 10 + 1
        else:
            page = total // 10
        for p in range(2, page + 1):  # 首页时已经过了一页了，所以从第二页开始
            meta_copy = meta.copy()
            meta_copy.update(pageIndex=p)
            yield ReSpider.Request(
                url='http://qikan.cqvip.com/Article/SingleDetail',
                method='POST',
                headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                         'Host': 'qikan.cqvip.com',
                         'Origin': 'http://qikan.cqvip.com',
                         'Referer': meta_copy.get('url')},
                data={
                    'id': meta_copy.get('id'),
                    'pageIndex': p,
                    'pageSize': 10,
                    'typeName': 'ckwx'
                },
                retry=True,
                # max_retry_times=10,
                do_filter=False,
                meta=meta_copy,
                priority=0,
                callback=self.parse2
            )

    async def parse2(self, response):
        meta = response.meta
        data_list = item.DataListItem(collection=self.saveDB)
        article_list_nodes = response.xpath('//li')
        for article_list_node in article_list_nodes:
            article_ = article_list_node.xpath('.//text()').getall()
            article_ = [a.strip() for a in article_ if a.strip() != '']
            article = ' '.join(article_)
            data = dict(aid=meta.get('id'),
                        url=meta.get('url'),
                        yinwen=article,
                        byl=meta.get('byl'))
            self.logger.info(data)
            data_list.append(data)
        yield data_list


if __name__ == '__main__':
    ReferenceByApi().start()
