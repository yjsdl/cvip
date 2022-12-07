# -*- coding: utf-8 -*-
# @Time    : 2022/03/03 15:22
# @Author  : PC-006
# @File    : ${file_name}.py

import ReSpider
from ReSpider import item
import json
from ReSpider.utils.urlProcess import urlParse
import math
from copy import deepcopy


# from ReSpider.core.downloader.handlers import DownloadHandler


class QikanSpider(ReSpider.Spider):
    __custom_setting__ = {
        'TASK_LIMIT': 4,
        'DOWNLOAD_DELAY': 0,
        'DOWNLOADER_MIDDLEWARES': {
            # 'cqVIP.middleware.Rs5CookieMiddleware': 5
            'cqVIP.middleware.Rs5CookiePostMiddleware': 5
        }
    }
    search_api = 'http://qikan.cqvip.com/Search/SearchList'

    def start_requests(self):
        yield ReSpider.Request(
            url='http://qikan.cqvip.com/Qikan/Journal/JournalGuid?from=Qikan_Journal_JournalGuid'
        )

    def parse(self, response):
        """
        目的是拿到所以的期刊门类
        :param response:
        :return:
        """
        li_info = response.xpath('//*[@id="searchlist"]/div[2]/div[3]/h2/span[@class="title"]/a')
        for li in li_info:
            title = li.xpath('./@title').get()
            href = response.urljoin(li.xpath('./@href').get())
            info = {
                'title': title,
                'href': href
            }
            self.logger.debug(info)
            yield ReSpider.Request(
                url=href,
                timeout=30,
                do_filter=True,
                retry=True,
                max_retry_times=10,
                meta=info,
                callback=self.parse2
            )

    def parse2(self, response):
        """
        拿到
        :param response:
        :return:
        """
        meta = response.meta
        if meta.get('MAX_PAGE') is None:  # 在第一页把meta传基础值
            search_param = response.xpath('//input[@name="preSearchParamModelJson"]/@value').get()
            search_param = json.loads(search_param)
            user_id = response.re_first(r'objLog\.user_id = (.*?);')
            pages = math.ceil(search_param.get('ShowTotalCount', 0) / 100)
            if search_param.get('ShowTotalCount', 0) > 20:
                meta.update(page=0, TOTAL_COUNT=search_param['ShowTotalCount'], MAX_PAGE=pages, USER_ID=user_id,
                            ZY=search_param.get('UrlParam'))
            else:
                meta.update(page=1, TOTAL_COUNT=search_param['ShowTotalCount'], MAX_PAGE=pages, USER_ID=user_id,
                            ZY=search_param.get('UrlParam'))
        tr_nodes = response.xpath('//*[@id="coverlist"]/div/dl')
        csv_list = item.CSVListItem(data_directory='F:/工作数据存储2022/20220425_维普下载需求/', filename='期刊列表')
        for tr_node in tr_nodes:
            link = response.urljoin(tr_node.xpath('./dt/a/@href').get())
            kanming = tr_node.xpath('./dt/a/text()').get()
            id_ = urlParse(link)['gch']
            kan = {'id': id_, '刊名': kanming, '链接': link}
            kan.update(meta)
            self.logger.debug(kan)
            csv_list.append(kan)
            yield ReSpider.Request(
                url=link,
                timeout=30,
                retry=True,
                max_retry_times=5,
                priority=0,
                meta=kan,
                callback=self.qikan_parse
            )
        yield csv_list
        if meta.get('page') < meta['MAX_PAGE']:
            meta_copy = deepcopy(meta)
            page = meta_copy['page'] + 1
            meta_copy.update(page=page)
            payload = {
                'searchParamModel': json.dumps(
                    {"ObjectType": 7, "SearchKeyList": [], "SearchExpression": None, "BeginYear": None, "EndYear": None,
                     "UpdateTimeType": None, "JournalRange": None, "DomainRange": None,
                     "ClusterFilter": meta['ZY'] + '#' + meta['title'],
                     "ClusterLimit": 0, "ClusterUseType": "Article", "UrlParam": "", "Sort": "1", "SortField": None,
                     "UserID": meta['USER_ID'], "PageNum": str(page), "PageSize": 100, "SType": None, "StrIds": None,
                     "IsRefOrBy": 0,
                     "ShowRules": "", "IsNoteHistory": 0, "AdvShowTitle": None, "ObjectId": None, "ObjectSearchType": 0,
                     "ChineseEnglishExtend": 0, "SynonymExtend": 0, "ShowTotalCount": meta['TOTAL_COUNT'],
                     "AdvTabGuid": ""},
                    ensure_ascii=False
                )
            }
            yield ReSpider.Request(
                url=self.search_api,
                method='POST',
                data=payload,
                do_filter=True,
                timeout=60,
                retry=True,
                max_retry_times=10,
                meta=meta_copy,
                callback=self.parse2
            )

    def qikan_parse(self, response):
        meta = response.meta
        yield item.FileItem(response.text, data_directory='H:/维普期刊', filename=meta['刊名'], filetype='html')
        """
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
            max_retry_times=10,
            meta=meta,
            callback=self.qikan_list_parse
        )
        """

    def qikan_list_parse(self, response):
        meta = response.meta
        title = response.xpath('//*[@id="remark"]/dl/dt/a/text()').getall()
        aid = response.xpath('//*[@id="remark"]/dl/dt/a/@articleid').getall()
        click_list: list = response.xpath('//*[@id="remark"]/dl/dd/div/a[2]/@onclick').re(r'(.*?)\(')
        # if click.find('showdown'):
        # print(click_list)
        # meta.update({'title': title, 'aid': aid})
        csv_item = item.CSVItem(data_directory='F:/工作数据存储2022/20220425_维普下载需求/', filename='维普验证')
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
    QikanSpider().start()
