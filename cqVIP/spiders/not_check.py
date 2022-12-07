# -*- coding: utf-8 -*-
# @Time    : 2022/3/8 17:35
# @Author  : ZhaoXiangPeng
# @File    : not_check.py

import ReSpider
from ReSpider import item
import pandas as pd
import json


class NotCheck(ReSpider.Spider):
    __custom_setting__ = {
        'TASK_LIMIT': 2,
        'DOWNLOAD_DELAY': 0,
        'DOWNLOADER_MIDDLEWARES': {
            'cqVIP.middleware.Rs5CookieMiddleware': 5
            # 'cqVIP.middleware.Rs5CookiePostMiddleware': 5
        }
    }
    search_api = 'http://qikan.cqvip.com/Search/SearchList'

    def start_requests(self):
        df = pd.read_excel('F:/工作数据存储2022/20220301_维普下载需求/未检查.xlsx', engine='openpyxl')
        # print(df)
        for x in df.iterrows():
            id_, kanming, link = x[1]
            kan = {'id': id_, '刊名': kanming, '链接': link}
            yield ReSpider.Request(
                url=link,
                timeout=30,
                retry=True,
                max_retry_times=5,
                meta=kan,
                callback=self.qikan_parse
            )

    def qikan_parse(self, response):
        meta = response.meta
        yield item.FileItem(response.text, data_directory='H:/维普期刊', filename=meta['刊名'], filetype='html')
        title = response.xpath('//*[@id="body"]/div/div/div[1]/div[1]/h1/text()').get()
        total = response.xpath('//*[@id="body"]/div/div/div[1]/div[3]/span[1]/a/text()').get()
        journalid = response.xpath('//*[@id="body"]/div/div/div[1]/div[2]/a[1]/@data-journalid').get()
        issn = response.xpath('//*[@id="body"]/div/div/div[1]/ul/li[@class="issn"]/text()').get()  # issn
        cn = response.xpath('//*[@id="body"]/div/div/div[1]/ul/li[@class="cn"]/text()').get()  # issn
        meta.update({'total': total, 'journalid': journalid, 'issn': issn, 'cn': cn})
        self.logger.debug(title)
        user_id = response.re_first(r'objLog\.user_id = (.*?);')
        payload2 = {
            'searchParamModel': json.dumps({"ObjectType": 1, "SearchKeyList": [
                {"FieldIdentifier": "MCC", "SearchKey": journalid, "PreLogicalOperator": None,
                 "AfterLogicalOperator": None, "LeftBracket": None, "RighgtBracket": None, "IsExact": None,
                 "ClusterShowName": None}], "SearchExpression": None, "BeginYear": None, "EndYear": None,
                                            "UpdateTimeType": None, "JournalRange": None, "DomainRange": None,
                                            "ClusterFilter": "YY=2021#2021", "ClusterLimit": 0,
                                            "ClusterUseType": "Journal", "UrlParam": "", "Sort": "0", "SortField": None,
                                            "UserID": user_id, "PageNum": 1, "PageSize": 20, "SType": None,
                                            "StrIds": None, "IsRefOrBy": 0, "ShowRules": f"  期刊={meta['刊名']}  ",
                                            "IsNoteHistory": 0, "AdvShowTitle": None, "ObjectId": None,
                                            "ObjectSearchType": 0, "ChineseEnglishExtend": 0, "SynonymExtend": 0,
                                            "ShowTotalCount": total, "AdvTabGuid": ""},
                                           ensure_ascii=False)
        }
        yield ReSpider.Request(
            url=self.search_api,
            method='POST',
            data=payload2,
            timeout=60,
            retry=True,
            priority=0,
            max_retry_times=10,
            meta=meta,
            callback=self.qikan_list_parse
        )

    def qikan_list_parse(self, response):
        meta = response.meta
        title = response.xpath('//*[@id="remark"]/dl/dt/a/text()').getall()
        aid = response.xpath('//*[@id="remark"]/dl/dt/a/@articleid').getall()
        click_list: list = response.xpath('//*[@id="remark"]/dl/dd/div/a[2]/@onclick').re(r'(.*?)\(')
        # if click.find('showdown'):
        # print(click_list)
        # meta.update({'title': title, 'aid': aid})
        csv_item = item.CSVItem(data_directory='F:/工作数据存储2022/20220301_维普下载需求/', filename='维普验证2')
        if click_list.__len__() > 0:
            self.logger.info(f'{meta["刊名"]} 可以下载')
            meta.update({'是否可下载': '是'})
            csv_item.update(meta)
            yield csv_item
        else:
            self.logger.info(f'{meta["刊名"]} 不可下载')
            meta.update({'是否可下载': '否'})
            csv_item.update(meta)
            yield csv_item


if __name__ == '__main__':
    NotCheck().start()
