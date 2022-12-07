# -*- coding: utf-8 -*-
# @Time    : 2022/1/12 14:55
# @Author  : ZhaoXiangPeng
# @File    : 表头处理.py

import pandas as pd
import os


def process_one(file: str):
    df = pd.read_excel(file, engine='openpyxl')
    # df = pd.read_csv(file)
    new_columns = [c.strip().replace(' ', '').replace('\u3000', '') for c in df.columns.values.tolist()]
    # print(new_columns)
    df.columns = new_columns
    # print(df)
    df.to_excel(file, index=False)
    # df.to_csv(file, index=False)


def get_files(path):
    fs = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if '.xlsx' in file:
                fs.append(os.path.join(root, file))
    return fs


def batch_process():
    files = get_files(root1)
    for file in files:
        process_one(file)


if __name__ == '__main__':
    root1 = 'F:/工作数据存储2022/20220105_上海外国语大学CSSCI/'
    batch_process()
    process_one(r'F:\工作数据存储2022\20220301_ers数据更新\cqvip2022年\中国地质大学(武汉)2022中文发文.csv')
