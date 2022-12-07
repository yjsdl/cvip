# -*- coding: utf-8 -*-
# @Time    : 2022/03/08 10:21
# @Author  : PC-006
# @File    : qikan_search.py

import ReSpider
from ReSpider.utils.urlProcess import quote_url
from ReSpider import item
from cqVIP.util.SearchParamModel import SearchParamModel
import json
import math
import re
from copy import deepcopy


class QikanSearch(ReSpider.Spider):
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

    def start_requests(self):
        # '中国地质大学（武汉）'
        # for school in ['四川大学', '南京师范大学', '南京中医药大学', '上海电力大学', '华中农业大学', '中欧国际工商学院', '中南财经政法大学', '浙江大学', '同济大学', '上海外国语大学', '上海工程技术大学', '上海财经大学', '江汉大学', '华中科技大学', '华东师范大学', '华东理工大学', '三峡大学', '长安大学', '西安电子科技大学', '西安建筑科技大学', '重庆交通大学', '西南交通大学', '西南财经大学', '电子科技大学', '西北工业大学', '西安交通大学', '陕西师范大学', '西南民族大学', '西南科技大学', '兰州大学', '西北师范大学', '中国人民大学', '中国农业大学', '郑州大学', '天津大学', '首都医科大学', '首都师范大学', '北京科技大学', '三江学院', '中国矿业大学', '扬州大学', '苏州大学', '中国科学技术大学', '清华大学', '南京医科大学', '南京审计大学', '南京农业大学', '南京林业大学', '南京航空航天大学', '南京工业大学', '南京工程学院', '南京大学', '南京财经大学', '江苏师范大学', '江苏大学', '江南大学', '河海大学', '合肥工业大学', '东南大学', '常州大学', '安徽医科大学', '安徽建筑大学', '曲阜师范大学']:
        for school in ['北京理工大学']:
            for year in range(2020, 2023):
            # for year in [i for i in range(1987, 2001)]:  #+[1953, 1955, 1959, 1960,1965]:  # + [i for i in range(1974, 1978)]+[1959,1965,1966]:
                param = dict(search_key=school, start_year=year, end_year=year, page_num=1, page_size=100, year=year)
                yield ReSpider.Request(
                    url='http://qikan.cqvip.com/Search/SearchList',
                    method='POST',
                    data=self.searchParam(search_key=school, start_year=year, end_year=year, page_num=1, page_size=100),
                    retry=True,
                    meta=param
                )

    def parse(self, response):
        meta = response.meta
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
        # 新任务逻辑
        if meta.get('MAX_PAGE') is None:
            # 翻页逻辑
            total_count = response.xpath('//input[@id="hidShowTotalCount"]/@value').get()
            total_count = int(total_count)
            self.logger.info('%s [%s-%s] 年 %s 找到 %s 篇文章' % (meta['search_key'], meta['start_year'], meta['end_year'], meta.get('cluster_filter', ''), total_count))
            meta['MAX_PAGE'] = math.ceil(total_count/100)

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
                for p in range(2, meta['MAX_PAGE']+1):
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

    def fetch_parse(self, response):
        meta = response.meta
        row_nodes = response.xpath('//ul[@id="classCluster"]/li')
        for row_node in row_nodes:
            search = row_node.xpath('./a/@data-search').get()  # 二级筛选值
            total_count = row_node.xpath('./a/tt/text()').get().replace(',', '')
            total_count = int(total_count)
            meta_copy = deepcopy(meta)
            # meta_copy['MAX_PAGE'] = math.ceil(total_count / 100)  # >5000
            meta_copy.update(cluster_filter=search)
            searchParamModel = SearchParamModel(**meta_copy)
            yield ReSpider.Request(
                url=self.search,
                method='POST',
                data={'searchParamModel': searchParamModel()},
                meta=meta_copy,
                callback=self.parse
            )

    def export_parse(self, response):
        meta = response.meta
        # response.re()
        # columns = re.findall(r"<Row ss:AutoFitHeight='0'>.*?</Row>", response.text)
        # columns = re.findall(r'<Data ss:Type=\'String\'>(.*?)</Data>', columns[0])
        # table_head = [c.strip().replace(' ', '').replace('\u3000', '') for c in columns]
        rows = re.findall(r'<Row ss:AutoFitHeight=\'1\'>(.*?)</Row>', response.text)
        data_list = item.CSVListItem(data_directory=f'E:/Juntu2022/cqVIP/{meta["search_key"]}/', filename=f'{meta["search_key"]}{meta["year"]}中文发文')
        # data_list = item.CSVListItem(data_directory='F:/工作数据存储2022/20220301_ers发文更新/cqvip/', filename=f'{meta["search_key"]}{meta["year"]}中文发文')
        # data_list = item.MysqlListItem(table='data_cqvip_post')
        for row in rows:
            items = re.findall(r'<Data ss:Type=\'String\'>(.*?)</Data>', row)
            data_list.append(dict(zip(self.table_head, items)))
        yield data_list

    def searchParam(self,
                 field: str = '机构',  # 搜索字段
                 search_key: str = None,  # 搜索词
                 start_year: int = 2022, end_year: int = 2022,
                 page_num: int = 1, page_size: int = 20,
                 **kwargs):
        if search_key is None:
            raise ValueError("search_key 不能为空")
        show_rules = f"  {field}={search_key}   AND (years:[{start_year} TO {end_year}])"
        adv_show_title = field+'='+search_key+' AND 年份：'+str(start_year)+'-'+str(end_year)
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


if __name__ == '__main__':
    QikanSearch().start()
