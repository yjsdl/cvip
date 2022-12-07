# -*- coding: utf-8 -*-
# @Time    : 2021/11/8 17:00
# @Author  : ZhaoXiangPeng
# @File    : 转换xlsx.py

import pandas as pd
import os
import re


def join_excel():
    file_path = 'H:/cqVIP/{}/2021.xlsx'
    # file_list = ['南京师范大学', '南京审计大学', '三江学院', '中国科学技术大学', '合肥工业大学', '三峡大学', '北京科技大学', '曲阜师范大学', '四川大学', '西安建筑科技大学', '西安电子科技大学', '长安大学']
    file_list = ['江苏大学']
    df = pd.DataFrame()
    for file_ in file_list:
        file = file_path.format(file_)
        print(file)
        df_ = pd.read_excel(file, engine='openpyxl')
        df = df.append(df_)
    print(df)
    df.to_csv('F:/工作数据存储2022/20220224_江苏大学2021中文发文/P1.CSV', index=False)


def join_csv(file_path: str = None, file_list: list = None):
    for file_ in file_list:
        df = pd.DataFrame()
        FILE_LIST = []
        file_path_ = file_path.format(file_)
        for root, dirs, files in os.walk(file_path_):
            for f in files:
                if re.search(r'.*?(20|21|22)中文发文.csv', f) is not None:
                    FILE_LIST.append(os.path.join(root, f))
        for FILE in FILE_LIST:
            print('当前合并 %s' % FILE)
            df_ = pd.read_csv(FILE, engine='python')
            df = df.append(df_)
        print(df)
        df['序号'] = 1
        df.drop_duplicates(inplace=True)
        df.to_csv(file_path_ + f'/{file_}output.csv', index=False)


if __name__ == '__main__':
    # join_csv('F:/工作数据存储2022/20220301_ers数据更新/{}', ['cqvip2022年'])
    join_csv('H:/数据科学平台/{}/', ['西北工业大学'])
