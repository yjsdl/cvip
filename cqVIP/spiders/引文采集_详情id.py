# 模拟浏览器采集维普引文
import ReSpider
from ReSpider import item
from lxml import etree
import pandas as pd
import pymongo


clint = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = clint.data_temp


class CQVipQuotation(ReSpider.Spider):
    name = 'cqvip_quotation'
    saveDB = 'data_weipu_hncssci2021'

    def __init__(self):
        super().__init__(name=self.name)
        self.settings.update({'TASK_LIMIT': 6})
        self.settings.update({'SCHEDULER': 'ReSpider.extend.redis.scheduler.RedisScheduler'})
        # self.settings.get('DOWNLOADER_MIDDLEWARES', {}).update(
        #     {'ReSpider.extend.puppeteer.downloadmiddleware.PuppeteerMiddleware': 6})

    def start_requests(self):
        temp1 = db[self.saveDB].distinct("url")
        print(len(temp1))
        # df = pd.read_csv(r'F:\工作数据存储2022\20220105_上海外国语大学CSSCI\二次处理\2020.CSV')
        df = pd.read_excel(r'F:\工作数据存储2022\20220105_华中农业大学CSSCI\二次处理\cssci错误.xlsx', engine='openpyxl')
        df.dropna(subset=['网　址'], inplace=True)
        URLS = df['网　址'].values.tolist()
        URLS = set(URLS) - set(temp1)
        print(len(URLS))
        for url in URLS:
            # print(url)
            # url = 'http://qikan.cqvip.com/Qikan/Article/Detail?id=7103169735'
            yield ReSpider.PuppeteerRequest(
                url=url,
                wait_until='networkidle2',
                do_filter=True,
                meta={'url': url,
                      'id': url.split('=')[-1]},
                callback=self.parse  # 第一次取cookie
            )

    async def parse(self, response):
        # 引文 被引量解析
        meta = response.meta
        # print(response.text)
        cookiejar = response.cookies
        cookies = []
        for c in cookiejar:
            cookies.append(f'{c["name"]}={c["value"]}')
        cookie = '; '.join(cookies)
        self.logger.info('parse cookie -> %s' % cookie)
        # html = etree.HTML(response.content)
        byl = response.xpath('//div[@id="body"]/div/div/div[1]/div[1]/h1/span[@class="cited"]/a/text()').get()
        article_list_nodes = response.xpath(
            '//div[@id="referenceRelate"]/div[@class="relate"]/div[@class="article-list"]/ul[@id="referenceRelateInfo"]/li')
        # byl = byl[0] if byl else 0
        meta.update(byl=byl)
        # csv_item = item.CSVItems(data_directory='')
        for article_list_node in article_list_nodes:
            article_ = article_list_node.xpath('.//text()').getall()
            article_ = [a.strip() for a in article_ if a.strip() != '']
            article = ' '.join(article_)
            data_item = item.DataItem(collection=self.saveDB)
            data_item.update(aid=meta.get('id'),
                             url=meta.get('url'),
                             yinwen=article,
                             byl=byl)
            self.logger.info(data_item)
            yield data_item
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
                         'Cookie': cookie,
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
                do_filter=True,
                meta=meta_copy,
                priority=0,
                callback=self.parse2
            )

    async def parse2(self, response):
        meta = response.meta
        # print(meta)
        self.logger.debug(response)
        # print(response.text)
        if response.status == 412:
            self.logger.info(meta)
            yield ReSpider.PuppeteerRequest(
                url=meta.get('url'),
                do_filter=False,
                priority=0,
                wait_until='networkidle2',
                meta=meta,
                callback=self.retry
            )
        else:
            # html = etree.HTML(response.content.decode('utf-8'))
            article_list_nodes = response.xpath('//li')
            for article_list_node in article_list_nodes:
                article_ = article_list_node.xpath('.//text()').getall()
                article_ = [a.strip() for a in article_ if a.strip() != '']
                article = ' '.join(article_)
                data_item = item.DataItem(collection=self.saveDB)
                data_item.update(aid=meta.get('id'),
                            url=meta.get('url'),
                            yinwen=article,
                            byl=meta.get('byl'))
                self.logger.info(data_item)
                yield data_item

    async def parse3(self, response):
        meta = response.meta
        # print(response.text)
        cookiejar = response.cookies
        cookies = []
        for c in cookiejar:
            cookies.append(f'{c["name"]}={c["value"]}')
        cookie = '; '.join(cookies)
        self.logger.debug('parse cookie -> %s' % cookie)
        html = etree.HTML(response.content)
        byl = html.xpath('//div[@id="body"]/div/div/div[1]/div[1]/h1/span[@class="cited"]/a/text()').getall()
        data_item = item.DataItem(collection=self.saveDB)
        data_item.update(aid=meta.get('id'),
                    url=meta.get('url'),
                    byl=byl[0] if byl else 0)
        self.logger.info(data_item)
        yield data_item

    async def retry(self, response):
        meta = response.meta
        self.logger.info('retry....')
        # print(meta)
        cookiejar = response.cookies
        cookies = []
        for c in cookiejar:
            cookies.append(f'{c["name"]}={c["value"]}')
        cookie = '; '.join(cookies)
        self.logger.debug('retry cookies -> %s' % cookie)
        yield ReSpider.Request(
            url='http://qikan.cqvip.com/Article/SingleDetail',
            method='POST',
            headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                     'Cookie': cookie,
                     'Host': 'qikan.cqvip.com',
                     'Origin': 'http://qikan.cqvip.com',
                     'Referer': meta.get('url')},
            data={
                'id': meta.get('id'),
                'pageIndex': meta.get('pageIndex'),
                'pageSize': 10,
                'typeName': 'ckwx'
            },
            retry=True,
            do_filter=False,
            meta=meta,
            priority=0,
            callback=self.parse2
        )


if __name__ == '__main__':
    CQVipQuotation().start()
