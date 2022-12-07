# -*- coding: utf-8 -*-
# @Time    : 2022/3/25 10:51
# @Author  : ZhaoXiangPeng
# @File    : del_error_row.py


import pymongo

clint = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = clint.data_temp
collection = db['data_weipu_ers']
ids = ['7104670553', '7106188293', '7103769791', '7105048438', '7105514995', '7103792714', '7106166390', '7104931988', '7104204436', '7103881222', '7103930423', '7105008422', '7105753849', '7104553533', '7105188812', '7103745355', '7104314146', '7105355233', '7104944350']
for id_ in ids[1:]:
    res = collection.remove({'aid': id_})
    print(id_, ': ', res)
