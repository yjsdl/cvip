# -*- coding: utf-8 -*-
# @Time    : 2022/10/21 09:04
# @Author  : crab-pc
# @File    : test.py

import ReSpider
from ReSpider import item


class Test(ReSpider.Spider):
    __custom_setting__ = {
        'TASK_LIMIT': 2,
    }
    start_urls = []

    def start_requests(self):
        for i in range(1, 2):
            yield ReSpider.Request(
                url='https://www.baidu.com',
                # proxy='https://127.0.0.1:1080'
            )

    def parse(self, response):
        print(response.status)
        aaa = {
            'title_name': 'Mechanism of piR-1245/PIWI-like protein-2 regulating Janus kinase-2/signal transducer and activator of transcription-3/vascular endothelial growth factor signaling pathway in retinal neovascularization',
            'author': 'Yong Yu;Li-Kun Xia;Yu Di;Qing-Zhu Nie;Xiao-Long Chen;Department of Ophthalmology, Shengjing Hospital of China Medical University;',
            'abstract': 'Inhibiting retinal neovascularization is the optimal strategy for the treatment of retina-related diseases, but there is currently no effective treatment for retinal neovascularization. P-element-induced wimpy testis（PIWI）-interacting RNA（piRNA） is a type of small non-coding RNA implicated in a variety of diseases. In this study, we found that the expression of piR-1245 and the interacting protein PIWIL2 were remarkably increased in human retinal endothelial cells cultured in a hypoxic environment, and cell apoptosis, migration, tube formation and proliferation were remarkably enhanced in these cells. Knocking down piR-1245 inhibited the above phenomena. After intervention by a p-JAK2 activator, piR-1245 decreased the expression of hypoxia inducible factor-1α and vascular endothelial growth factor through the JAK2/STAT3 pathway. For in vivo analysis, 7-day-old newborn mice were raised in 75 ± 2% hyperoxia for 5 days and then piR-1245 in the retina was knocked down. In these mice, the number of newly formed vessels in the retina was decreased, the expressions of inflammationrelated proteins were reduced, the number of apoptotic cells in the retina was decreased, the JAK2/STAT3 pathway was inhibited, and the expressions of hypoxia inducible factor-1α and vascular endothelial growth factor were decreased. Injection of the JAK2 inhibitor JAK2/TYK2-IN-1 into the vitreous cavity inhibited retinal neovascularization in mice and reduced expression of hypoxia inducible factor-1α and vascular endothelial growth factor. These findings suggest that piR-1245 activates the JAK2/STAT3 pathway, regulates the expression of hypoxia inducible factor-1α and vascular endothelial growth factor, and promotes retinal neovascularization. Therefore, piR-1245 may be a new therapeutic target for retinal neovascularization.',
            'keywords': 'angiogenesis;\rhumanretinalendothelialcells;\rhypoxiainduciblefactor-1α;\rhypoxia;\rinterleukin-1β;\rmigration;\rnon-codingRNA;\roxygen-inducedinjury;\rPIWI-interactingRNA;\rretinopathy;\r',
            'fund': 'supportedbytheNationalNaturalScienceFoundationofChina,No.81570866（toXLC）；\r', 'doi': '',
            'series': '(E) Medicine ＆ Public Health', 'subject': 'Ophthalmology and Otolaryngology', 'clc': 'R774.1',
            'journal_name': '中国神经再生研究(英文版).\r;2023(05)\r;\rPage:1132-1138'}
        data_list = item.CSVListItem(data_directory='./', filename='测试存储')
        data = item.DataItem()
        data_list.append(aaa)
        yield data_list


if __name__ == '__main__':
    Test().start()
    file_names = ['A8 马克思主义、列宁主义、毛泽东思想、邓小平理论的学习和研究.csv', 'B84 心理学.csv', 'C91 社会学.csv', 'C93 管理学.csv', 'C95 民族学.csv',
                  'D631 公安工作.csv', 'D9 法律.csv', 'D917 犯罪学.csv', 'D918 刑事侦查学（犯罪对策学、犯罪侦查学）.csv', 'E22 政治工作.csv',
                  'E251 军事教育、军事训练.csv', 'E29 军事史（战史、建军史）.csv', 'F3 农业经济.csv', 'F323.2 农业资源开发与利用.csv', 'F326.2 林业.csv',
                  'G2 信息与知识传播.csv', 'G250 图书馆学.csv', 'G27 档案学、档案事业.csv', 'G35 情报学、情报工作.csv', 'G4 教育.csv', 'G8 体育.csv',
                  'H1 汉语.csv', 'H3 常用外国语.csv', 'I2 中国文学.csv', 'J 艺术.csv', 'J0 艺术理论.csv', 'J6 音乐.csv', 'J8 戏剧艺术.csv',
                  'J9 电影、电视艺术.csv', 'K092 中国.csv', 'K1 世界史.csv', 'K2 中国史.csv', 'K9 地理.csv', 'O1 数学.csv', 'O3 力学.csv',
                  'O4 物理学.csv', 'O43 光学.csv', 'O6 化学.csv', 'O7 晶体学.csv', 'P1 天文学.csv', 'P2 测绘学.csv', 'P3 地球物理学.csv',
                  'P4 大气科学（气象学）.csv', 'P5 地质学.csv', 'P61 矿床学.csv', 'P62 地质、矿产普查与勘探.csv', 'P7 海洋学.csv', 'P75 海洋工程.csv',
                  'P9 自然地理学.csv', 'Q 生物科学.csv', 'Q81 生物工程学（生物技术）.csv', 'R1 预防医学、卫生学.csv', 'R2 中国医学.csv', 'R28 中药学.csv',
                  'R3 基础医学.csv', 'R318 生物医学工程.csv', 'R4 临床医学.csv', 'R47 护理学.csv', 'R6 外科学.csv', 'R71 妇产科学.csv',
                  'R72 儿科学.csv', 'R74 神经病学与精神病学.csv', 'R75 皮肤病学与性病学.csv', 'R77 眼科学.csv', 'R78 口腔科学.csv', 'R8 特种医学.csv',
                  'R9 药学.csv', 'S157 水土保持.csv', 'S2 农业工程.csv', 'S4 植物保护.csv', 'S5 农作物.csv', 'S54 饲料作物、牧草.csv',
                  'S6 园艺.csv', 'S68 观赏园艺（花卉和观赏树木）.csv', 'S7 林业.csv', 'S8 畜牧、动物医学、狩猎、蚕、蜂.csv', 'S85 动物医学（兽医学）.csv',
                  'S9 水产、渔业.csv', 'TB472 产品设计.csv', 'TB6 制冷工程.csv', 'TD 矿业工程.csv', 'TD1 矿山地质与测量.csv', 'TE 石油、天然气工业.csv',
                  'TF 冶金工业.csv', 'TH 机械、仪表工业.csv', 'TK 能源与动力工程.csv', 'TL 原子能技术.csv', 'TM 电工技术.csv',
                  'TN 无线电电子学、电信技术.csv', 'TN4 微电子学、集成电路（IC）.csv', 'TN91 通信.csv', 'TP13 自动控制理论.csv',
                  'TP273 自动控制、自动控制系统.csv', 'TP3 计算技术、计算机技术.csv', 'TP311.5 软件工程.csv', 'TQ 化学工业.csv', 'TQ92 发酵工业.csv',
                  'TS1 纺织工业、染整工业.csv', 'TS2 食品工业.csv', 'TS5 皮革工业.csv', 'TS7 造纸工业.csv', 'TS941 服装工业.csv', 'TU 建筑科学.csv',
                  'TU98 区域规划、城乡规划.csv', 'TU986 园林规划与建设.csv', 'TV 水利工程.csv', 'U 交通运输.csv', 'U66 船舶工程.csv',
                  'X1 环境科学基础理论.csv', 'X171.4 生态建设与生态恢复.csv', 'X2 社会与环境.csv', 'X3 环境保护管理.csv', 'X32 环境规划与环境管理.csv',
                  'X5 环境污染及其防治.csv', 'X7 废物处理与综合利用.csv', 'X8 环境质量评价与环境监测.csv', 'X93 安全工程.csv']

    # a = file_names.index('X2 社会与环境.csv')
    # print(a)
    # import os
    # path = r'F:\my_workfiles\CNKI\CLC\file_in\\'
    # for i in range(0, 117):
    #     name = file_names[i]
    #     if os.path.exists(path + name):
    #         pass
    #     else:
    #         print(name)