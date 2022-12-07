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
from copy import deepcopy


class QikanQuerySearch(ReSpider.Spider):
    __custom_setting__ = {
        'TASK_LIMIT': 4,
        'DOWNLOAD_DELAY': 0,
        'DOWNLOADER_MIDDLEWARES': {
            'cqVIP.middleware.Rs5CookiePostMiddleware': 5,
            # 'cqVIP.middleware.RsProxyMiddleware': 7
        }
    }
    left_cluster = 'http://qikan.cqvip.com/Qikan/WebControl/LeftCluster'
    search = 'http://qikan.cqvip.com/Search/SearchList'
    export_excel = 'http://qikan.cqvip.com/Qikan/Search/ExportExcel'
    table_head = ['序号', '题名', '作者', '机构', '基金', '刊名', '年', '卷', '期', 'ISSN号', 'CN号', '页码', '关键词', '分类号', '文摘', '网址']
    data_save_path = 'E:/数据科学平台'

    def start_requests(self):
        school = '生物医学转化'
        param = dict(search_key=school, page_num=1, page_size=100)
        yield ReSpider.Request(
            url='http://qikan.cqvip.com/Search/SearchList',
            method='POST',
            data=self.searchParam(search_key=school, page_num=1, page_size=100),
            retry=True,
            meta=param
        )

    async def parse(self, response):
        meta = response.meta
        if meta.get('start_year'):  # 确定年份后才导出
            # 导出逻辑
            ids = []
            row_nodes = response.xpath('//*[@id="remark"]/dl')
            for row_node in row_nodes:
                ids.append(row_node.xpath('./dt[1]/a/@articleid').get())
            yield ReSpider.Request(
                url=self.export_excel,
                method='POST',
                data={'filename': '',
                      'content': json.dumps({"ids": ','.join(ids)}, ensure_ascii=False)},
                meta=meta,
                callback=self.export_parse
            )
        else:
            meta_copy = deepcopy(meta)
            data_source = response.re_first(r'var dataSource = \'(.*?)\';')  # 拿到页面的 dataSource, *必须
            searchParamModel = SearchParamModel(**meta_copy)
            data = {"dataSource": data_source, "searchParamModel": quote_url(searchParamModel())}
            meta_copy.update(fetch='year')
            yield ReSpider.Request(
                url=self.left_cluster,
                method='POST',
                data=data,
                meta=meta_copy,
                callback=self.fetch_parse
            )
        # 新任务逻辑
        if (meta.get('start_year')) and (meta.get('MAX_PAGE') is None):
            # 翻页逻辑
            total_count = response.xpath('//input[@id="hidShowTotalCount"]/@value').get()
            total_count = int(total_count)
            self.logger.info(
                '%s [%s-%s] 年 %s 找到 %s 篇文章' % (
                    meta['search_key'], meta['start_year'], meta['end_year'], meta.get('cluster_filter', ''),
                    total_count))
            meta['MAX_PAGE'] = math.ceil(total_count / 100)

            # 大于5000条需要再次筛选
            if (total_count > 5000) and (meta.get('cluster_filter') is None):
                # 筛选逻辑
                meta_copy = deepcopy(meta)
                del meta_copy['MAX_PAGE']  # 需要删除页码数，以便下次可以
                data_source = response.re_first(r'var dataSource = \'(.*?)\';')  # 拿到页面的 dataSource, *必须
                searchParamModel = SearchParamModel(**meta_copy)
                data = {"dataSource": data_source, "searchParamModel": quote_url(searchParamModel())}
                yield ReSpider.Request(
                    url=self.left_cluster,
                    method='POST',
                    data=data,
                    meta=meta_copy,
                    callback=self.fetch_parse
                )
            else:
                for p in range(2, meta['MAX_PAGE'] + 1):
                    meta_copy = deepcopy(meta)
                    meta_copy['page_num'] = p
                    searchParamModel = SearchParamModel(**meta_copy)
                    yield ReSpider.Request(
                        url='http://qikan.cqvip.com/Search/SearchList',
                        method='POST',
                        data={'searchParamModel': searchParamModel()},
                        retry=True,
                        meta=meta
                    )
        else:
            self.logger.info('开始二次筛选')

    def fetch_parse(self, response):
        meta = response.meta
        type_xpath = {
            'year': response.xpath('//ul[@id="yearCluster"]/li'),
            'class': response.xpath('//ul[@id="classCluster"]/li')
        }
        fetch_type = meta.pop('fetch', None)
        if fetch_type and (fetch_type == 'year'):
            row_nodes = type_xpath[fetch_type]  # 年份筛选
        else:
            row_nodes = type_xpath['class']  # 学科类别筛选
        for row_node in row_nodes:
            search = row_node.xpath('./a/@data-search').get()  # 二级筛选值
            total_count = row_node.xpath('./a/tt/text()').get().replace(',', '')
            type_name = row_node.xpath('./a/@title').get()
            total_count = int(total_count)
            meta_copy = deepcopy(meta)
            # meta_copy['MAX_PAGE'] = math.ceil(total_count / 100)  # >5000
            if fetch_type == 'year':
                meta_copy.update(cluster_filter=search, start_year=int(type_name), end_year=int(type_name))
            searchParamModel = SearchParamModel(**meta_copy)
            yield ReSpider.Request(
                url=self.search,
                method='POST',
                data={'searchParamModel': searchParamModel()},
                meta=meta_copy,
                callback=self.parse
            )

    def searchParam(self,
                    field: str = '机构',  # 搜索字段
                    search_key: str = None,  # 搜索词
                    start_year: int = '', end_year: int = '',
                    page_num: int = 1, page_size: int = 20,
                    **kwargs):
        if search_key is None:
            raise ValueError("search_key 不能为空")
        show_rules = f"  {field}={search_key}  "
        adv_show_title = field + '=' + search_key
        searchParamModel = {"ObjectType": 1, "SearchKeyList": [
            {"FieldIdentifier": "S", "SearchKey": search_key, "PreLogicalOperator": "", "AfterLogicalOperator": None,
             "LeftBracket": None, "RighgtBracket": None, "IsExact": "0", "ClusterShowName": None}],
                            "SearchExpression": "", "BeginYear": start_year, "EndYear": end_year, "UpdateTimeType": "",
                            "JournalRange": "", "DomainRange": "", "ClusterFilter": "", "ClusterLimit": 0,
                            "ClusterUseType": "Article", "UrlParam": "", "Sort": "0", "SortField": None,
                            "UserID": "0", "PageNum": page_num, "PageSize": page_size, "SType": "", "StrIds": "",
                            "IsRefOrBy": 0, "ShowRules": show_rules, "IsNoteHistory": 0,
                            "AdvShowTitle": adv_show_title, "ObjectId": "", "ObjectSearchType": 0,
                            "ChineseEnglishExtend": 0, "SynonymExtend": 0, "ShowTotalCount": 0,
                            "AdvTabGuid": "0657c5c3-5252-aca4-6bb9-5acfa34fa30a"}

        return {'searchParamModel': json.dumps(searchParamModel, ensure_ascii=False)}

    def export_parse(self, response):
        meta = response.meta
        # response.re()
        # columns = re.findall(r"<Row ss:AutoFitHeight='0'>.*?</Row>", response.text)
        # columns = re.findall(r'<Data ss:Type=\'String\'>(.*?)</Data>', columns[0])
        # table_head = [c.strip().replace(' ', '').replace('\u3000', '') for c in columns]
        rows = re.findall(r'<Row ss:AutoFitHeight=\'1\'>(.*?)</Row>', response.text)
        data_list = item.CSVListItem(data_directory=f'{self.data_save_path}/{meta["search_key"]}/',
                                     filename=f'{meta["search_key"]}{meta["start_year"]}-{meta["end_year"]}中文发文')
        # data_list = item.MysqlListItem(table='data_cqvip_post')
        for row in rows:
            items = re.findall(r'<Data ss:Type=\'String\'>(.*?)</Data>', row)
            data_list.append(dict(zip(self.table_head, items)))
        yield data_list


if __name__ == '__main__':
    QikanQuerySearch().start()
