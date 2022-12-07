# -*- coding: utf-8 -*-

import os
import pandas as pd


def alter_filename():
    pf = pd.read_csv('./学科统计.csv', dtype=str)['name'].values.tolist()
    pf1 = []
    for i in pf:
        if i not in pf1:
            pf1.append(i)
    for j in pf1[1:]:
        file_path = fr'F:\维普\学科\{j}\\'
        filenames = os.listdir(file_path)[0]
        last_name = filenames.replace('1', j)

        str1 = file_path + filenames
        str2 = file_path + last_name
        # print(filenames, last_name)
        os.rename(str1, str2)


def move_file():
    pf = pd.read_csv('./学科统计.csv', dtype=str)['name'].values.tolist()
    pf1 = []
    for i in pf:
        if i not in pf1:
            pf1.append(i)
    cc = ['考古学史和考古学理论', '专门史与整体史', '城乡生态环境与基础设施规划', '内科学', '儿科学']
    for c in cc:
        pf1.remove(c)

    for j in pf1[1:]:
        # print(j)
        path = fr'F:\维普\学科\{j}\{j}.csv'
        last_path = fr'F:\维普\学科1\{j}.csv'
        table_head = ['序号', '题名', '作者', '机构', '基金', '刊名', '年', '卷', '期', 'ISSN号', 'CN号', '页码', '关键词', '分类号', '文摘', '网址']
        a = pd.read_csv(last_path, dtype=str)
        # print(a.columns)
        if '序号' not in a.columns:
            print(j)
        # if a.shape[0] == 0:
        #     print('有一个文件', j)
        # if not os.path.exists(os.path.dirname(last_path)):
        #     os.makedirs(os.path.dirname(last_path))
        #
        # if a.values[0][1] != '题名':
        #     # print(a.values)
        #     a.to_csv(last_path, index=False, encoding='utf-8', header=table_head)
        # else:
        #     a.to_csv(last_path, index=False, encoding='utf-8')

move_file()