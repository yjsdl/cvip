# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @Time    : 2022/04/06 14:34
# @Author  : PC-006
# @File    : qikan_query_search.py

import ReSpider
from ReSpider.utils.urlProcess import quote_url
from ReSpider import item
from cqVIP.util.SearchParamModel import SearchParamModel
import json
import math
import re
import pandas as pd
from lxml import etree
from copy import deepcopy


class QikanQuerySearch(ReSpider.Spider):
    __custom_setting__ = {
        'TASK_LIMIT': 3,
        'DOWNLOAD_DELAY': 0,
        'DOWNLOADER_MIDDLEWARES': {
            'cqVIP.middleware.Rs5CookiePostMiddleware': 5,
            # 'cqVIP.middleware.RsProxyMiddleware': 7
        }
    }
    left_cluster = 'http://qikan.cqvip.com/Qikan/WebControl/LeftCluster'
    search = 'http://qikan.cqvip.com/Search/SearchList'
    export_excel = 'http://qikan.cqvip.com/Qikan/Search/ExportExcel'
    # table_head = ['序号', '题名', '作者', '机构', '基金', '刊名', '年', '卷', '期', 'ISSN号', 'CN号', '页码', '关键词', '分类号', '文摘', '网址']
    # data_save_path = 'E:/数据科学平台'
    id_list = []

    def start_requests(self):
        # sha = pf.shape[0]
        # for i in pf[0:1]:
        # K85 1989
        file_name = 'TS5 皮革工业'
        # E251 军事教育、军事训练 E29 军事史（战史、建军史）TD1 矿山地质与测量 TS5 皮革工业
        issn_name = file_name.split(' ')[0]
        # year = ''
        for year in range(2010, 2012):
            # year = 2021
            param = dict(field='分类号', year=year, start_year=year, end_year=year, search_key=issn_name, page_num=1, page_size=100, file_name=file_name)
            yield ReSpider.Request(
                url='http://qikan.cqvip.com/Search/SearchList',
                method='POST',
                data=self.searchParam(field='分类号', year=year, search_key=issn_name, page_num=1,
                                      page_size=100),
                retry=True,
                meta=param,
                # proxy='http://127.0.0.1:1080'
            )

    async def parse(self, response):
        meta = response.meta
        print(meta)
        ids = []
        row_nodes = response.xpath('//*[@id="remark"]/dl')
        for row_node in row_nodes:
            ids.append(row_node.xpath('./dt[1]/a/@articleid').get())

        # 进入详情页
        for id in ids:
            meta_copy = deepcopy(meta)
            yield ReSpider.Request(
                url=f'http://qikan.cqvip.com/Qikan/Article/Detail?id={id}',
                method='GET',
                retry=True,
                meta=meta_copy,
                callback=self.get_deatil_mes,
                # proxy='http://127.0.0.1:1080'
            )

        # # 新任务逻辑
        if meta.get('MAX_PAGE') is None:
            # 翻页逻辑
            total_count = response.xpath('//input[@id="hidShowTotalCount"]/@value').get()
            total_count = int(total_count)
            self.logger.info(
                '%s  %s 找到 %s 篇文章' % (
                    meta['search_key'], meta.get('year', ''),
                    total_count))
            meta['MAX_PAGE'] = math.ceil(total_count / 100)
            if meta['MAX_PAGE'] > 50:
                meta['MAX_PAGE'] = 50

            for p in range(2, meta['MAX_PAGE'] + 1):
                meta_copy = deepcopy(meta)
                meta_copy['page_num'] = p
                searchParamModel = SearchParamModel(**meta_copy)
                yield ReSpider.Request(
                    url='http://qikan.cqvip.com/Search/SearchList',
                    method='POST',
                    data={'searchParamModel': searchParamModel()},
                    retry=True,
                    priority=p,
                    meta=meta_copy,
                    # proxy='http://127.0.0.1:1080'
                )

    def get_deatil_mes(self, response):
        meta = response.meta

        res = etree.HTML(response.text)
        article = res.xpath('//div[@class="article-main"]')[0]

        title_zh = article.xpath('.//div[@class="article-title"]/h1/text()')[0] if article.xpath(
            './/div[@class="article-title"]/h1/text()') else ''
        title_zh = title_zh.replace('\n', '').replace('\r', '').replace(' ', '')
        print(title_zh)
        title_em = article.xpath('.//div[@class="article-title"]/em/text()')[0] if article.xpath(
            './/div[@class="article-title"]/em/text()') else ""

        abstract_zh = article.xpath('.//div/div[@class="abstract"]/span/span//text()')
        abstract_zh = ''.join(abstract_zh)
        abstract_em = article.xpath('.//div/div[@class="abstract"]/em/span//text()')
        abstract_em = ''.join(abstract_em)
        author_zh = article.xpath('.//div/div[@class="author"]/span/span//text()')
        author_zh = ';'.join(author_zh)
        author_em = article.xpath('.//div/div[@class="author"]/em/span/text()')[0] if article.xpath(
            './/div/div[@class="author"]/em/span/text()') else ''
        organ_zh = article.xpath('.//div/div[@class="organ"]/span/span//text()')
        organ_zh = ';'.join(organ_zh)
        organ_em = article.xpath('.//div/div[@class="organ"]/em/span/text()')[0] if article.xpath(
            './/div/div[@class="organ"]/em/span/text()') else ''

        journal_zh = article.xpath('.//div/div[@class="journal"]/span//text()')
        journal_zh = [i.replace('\n', '').replace('\r', '').replace(' ', '') for i in journal_zh]
        journal_zh = ';'.join(journal_zh)
        journal_em = article.xpath('.//div/div[@class="journal"]/em/text()')[0] if article.xpath(
            './/div/div[@class="journal"]/em/text()') else ''

        fund = article.xpath('.//div/div[@class="fund"]/span//text()')
        fund = ';'.join(fund)

        subject_zh = article.xpath('.//div/div[@class="subject"]/span//text()')
        subject_zh = ';'.join(subject_zh)
        subject_em = article.xpath('.//div/div[@class="subject"]/em/span/text()')
        subject_em = ';'.join(subject_em)

        clc = article.xpath('.//div/div[@class="class"]/span/a/text()')
        clc = [i.replace('\n', '').replace('\r', '').replace(' ', '') for i in clc]
        clc = ';'.join(clc)

        aaa = {'title_zh': title_zh, 'title_em': title_em, 'abstract_zh': abstract_zh, 'abstract_em': abstract_em,
               'author_zh': author_zh, 'author_em': author_em, 'organ_zh': organ_zh,
               'organ_em': organ_em, 'journal_zh': journal_zh, 'journal_em': journal_em, 'fund': fund,
               'subject_zh': subject_zh,
               'subject_em': subject_em, 'clc': clc}
        data_list = item.CSVListItem(data_directory=fr'E:/维普/file_in/{meta["file_name"]}',
                                     filename=rf'{meta["file_name"]}')
        data_list.append(aaa)
        yield data_list

    def searchParam(self,
                    field: str = '任意字段',  # 搜索字段
                    search_key: str = None,  # 搜索词
                    start_year: int = '', end_year: int = '',
                    year: int = '',
                    page_num: int = 1, page_size: int = 20,
                    **kwargs):
        if search_key is None:
            raise ValueError("search_key 不能为空")
        show_rules = f"  {field}={search_key}  "
        adv_show_title = field + '=' + search_key
        # 二次筛选年份
        ClusterFilter = f"YY={year}#{year}" if year else ""

        searchParamModel = {"ObjectType": 1, "SearchKeyList": [
            {"FieldIdentifier": "C", "SearchKey": search_key, "PreLogicalOperator": "", "AfterLogicalOperator": None,
             "LeftBracket": None, "RighgtBracket": None, "IsExact": "0", "ClusterShowName": None}],
                            "SearchExpression": "", "BeginYear": start_year, "EndYear": end_year, "UpdateTimeType": "",
                            "JournalRange": "", "DomainRange": "", "ClusterFilter": ClusterFilter, "ClusterLimit": 0,
                            "ClusterUseType": "Article", "UrlParam": "", "Sort": "2", "SortField": None,
                            "UserID": "0", "PageNum": page_num, "PageSize": page_size, "SType": "", "StrIds": "",
                            "IsRefOrBy": 0, "ShowRules": show_rules, "IsNoteHistory": 0,
                            "AdvShowTitle": adv_show_title, "ObjectId": "", "ObjectSearchType": 0,
                            "ChineseEnglishExtend": 0, "SynonymExtend": 0, "ShowTotalCount": 0,
                            "AdvTabGuid": "0657c5c3-5252-aca4-6bb9-5acfa34fa30a"}

        # # 搜索的第一页数据
        # searchParamModel = {"ObjectType": 1, "SearchKeyList": [
        #     {"FieldIdentifier": "C", "SearchKey": "E19", "PreLogicalOperator": "", "IsExact": "0"}],
        #                     "SearchExpression": "", "BeginYear": "2019", "EndYear": "2019", "JournalRange": "",
        #                     "DomainRange": "", "PageSize": "0", "PageNum": "1", "Sort": "0", "ClusterFilter": "",
        #                     "SType": "", "StrIds": "", "UpdateTimeType": "", "ClusterUseType": "Article",
        #                     "IsNoteHistory": 1, "AdvShowTitle": "分类号=E19 AND 年份：2019-2019", "ObjectId": "",
        #                     "ObjectSearchType": "0", "ChineseEnglishExtend": "0", "SynonymExtend": "0",
        #                     "ShowTotalCount": "0", "AdvTabGuid": "2486b037-4cb7-f5aa-0d07-c9ed2076c0cc"}
        #
        # # 翻页
        # searchParamModel = {"ObjectType": 1, "SearchKeyList": [
        #     {"FieldIdentifier": "C", "SearchKey": "E19", "PreLogicalOperator": "", "AfterLogicalOperator": None,
        #      "LeftBracket": None, "RighgtBracket": None, "IsExact": "0", "ClusterShowName": None}],
        #                     "SearchExpression": "", "BeginYear": "2019", "EndYear": "2019", "UpdateTimeType": "",
        #                     "JournalRange": "", "DomainRange": "", "ClusterFilter": "", "ClusterLimit": 0,
        #                     "ClusterUseType": "Article", "UrlParam": "", "Sort": "0", "SortField": None,
        #                     "UserID": "8637416", "PageNum": 2, "PageSize": 20, "SType": "", "StrIds": "",
        #                     "IsRefOrBy": 0, "ShowRules": "  分类号=E19   AND (years:[2019 TO 2019])", "IsNoteHistory": 0,
        #                     "AdvShowTitle": "分类号=E19 AND 年份：2019-2019", "ObjectId": "", "ObjectSearchType": 0,
        #                     "ChineseEnglishExtend": 0, "SynonymExtend": 0, "ShowTotalCount": 125,
        #                     "AdvTabGuid": "2486b037-4cb7-f5aa-0d07-c9ed2076c0cc"}

        return {'searchParamModel': json.dumps(searchParamModel, ensure_ascii=False)}


if __name__ == '__main__':
    QikanQuerySearch().start()
