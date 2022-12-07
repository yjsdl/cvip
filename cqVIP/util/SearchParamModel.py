# -*- coding: utf-8 -*-
# @Time    : 2022/3/14 11:16
# @Author  : ZhaoXiangPeng
# @File    : SearchParamModel.py

import json


AdvMap = {
    'U': '任意字段',
    'M': '题名或关键词',
    'K': '关键词',
    'A': '作者',
    'C': '分类号',
    'S': '机构',
    'J': '刊名',
    'F': '第一作者',
    'T': '题名',
    'R': '摘要',
}
AdvMap2 = {'任意字段': 'U', '题名或关键词': 'M', '关键词': 'K', '作者': 'A', '分类号': 'C', '机构': 'S', '刊名': 'J', '第一作者': 'F', '题名': 'T', '摘要': 'R'}


class SearchParamModel:
    field: str = '任意字段'
    search_key: str
    start_year: int = None
    end_year: int = None
    cluster_filter: str = ''
    page_num: int = 1
    page_size: int = 20,
    __searchParamModel: dict = None

    def __init__(self,
                 field: str = '任意字段',  # 搜索字段
                 search_key: str = None,  # 搜索词
                 query: str = None,  # 检索式
                 cluster_filter: str = None,  # 筛选
                 start_year: int = None, end_year: int = None,
                 page_num: int = 1, page_size: int = 20,
                 **kwargs):
        if not (search_key or query):
            raise ValueError("'search_key' 和 'query' 至少其中一个不能为空")
        self.query = query
        self.search_key = search_key
        self.field = field
        self.start_year = start_year
        self.end_year = end_year
        self.show_rules = f"  {field}={search_key}  "
        if self.start_year or self.end_year:
            self.show_rules += f"   AND (years:[{start_year} TO {end_year}]"
        self.adv_show_title = self.query or (field + '=' + search_key)
        self.page_num = page_num
        self.page_size = page_size
        if cluster_filter:
            self.cluster_filter = cluster_filter

    @property
    def searchParamModel(self):
        if self.__searchParamModel is None:
            self.__searchParamModel = {"ObjectType": 1, "SearchKeyList": [],
                                       "SearchExpression": "", "BeginYear": self.start_year, "EndYear": self.end_year,
                                       "UpdateTimeType": "",
                                       "JournalRange": "", "DomainRange": "", "ClusterFilter": self.cluster_filter,
                                       "ClusterLimit": 0,
                                       "ClusterUseType": "Article", "UrlParam": "", "Sort": "0", "SortField": None,
                                       "UserID": "0", "PageNum": self.page_num, "PageSize": self.page_size, "SType": "",
                                       "StrIds": "",
                                       "IsRefOrBy": 0, "ShowRules": self.show_rules, "IsNoteHistory": 0,
                                       "AdvShowTitle": self.adv_show_title, "ObjectId": "", "ObjectSearchType": 0,
                                       "ChineseEnglishExtend": 0, "SynonymExtend": 0, "ShowTotalCount": 0,
                                       "AdvTabGuid": "0657c5c3-5252-aca4-6bb9-5acfa34fa30a"}
        if self.search_key and not self.query:
            self.__searchParamModel['SearchKeyList'].append(
                {"FieldIdentifier": AdvMap2.get(self.field), "SearchKey": self.search_key,
                 "PreLogicalOperator": "",
                 "AfterLogicalOperator": None,
                 "LeftBracket": None, "RighgtBracket": None, "IsExact": "0",
                 "ClusterShowName": None}
            )
        else:
            self.__searchParamModel['SearchExpression'] = self.query

        return self.__searchParamModel

    def __str__(self):
        return json.dumps({'field': self.field, 'search_key': self.search_key,
                           'start_year': self.start_year, 'end_year': self.end_year,
                           'page_num': self.page_num, 'page_size': self.page_size,
                           'cluster_filter': self.cluster_filter}, ensure_ascii=False)

    __repr__ = __str__

    def __call__(self, *args, **kwargs):
        return json.dumps(
            self.searchParamModel,
            ensure_ascii=False
        )
