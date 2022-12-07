# -*- coding: utf-8 -*-
# @Time    : 2022/10/20 19:55
# @Author  : crab-pc
# @File    : clc_down.py

import os
import ReSpider
from ReSpider import item
from lxml import etree
import pandas as pd


class ClcDown(ReSpider.Spider):
    __custom_setting__ = {
        'TASK_LIMIT': 8,
        'DOWNLOAD_DELAY': 0,
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'Cookie': 'Ecp_ClientId=3220420165906692312; Ecp_ClientIp=58.212.197.233; cnkiUserKey=ee6aa094-fcc6-a640-b23b-10ad197d8a3b; UM_distinctid=1805942f889139-08460b80622352-6b3e555b-1fa400-1805942f88a19c; Ecp_loginuserbk=SJTU; ASPSESSIONIDQAQARSQB=IGLLNFLDHBJLFBNFBJCDKCHH; eng_k55_id=123103; ASP.NET_SessionId=ilohuot5qitecjljviujyzir; _pk_ref=%5B%22%22%2C%22%22%2C1663571791%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DqAyApXZe7PsZK9kKQnBIEEf99Su4R9AoFfYWu3EyTO7%26wd%3D%26eqid%3Daac36a410010483b000000046328174c%22%5D; _pk_id=1da07332-73dd-494e-b5d9-3a9b652545aa.1650445190.30.1663571791.1663571791.; ASPSESSIONIDQCSDQQTA=JACKACDCAOAFCOMKELGEGIIF; dstyle=listmode; dsorder=pubdate; ASPSESSIONIDQCQBRTSB=KFFFOMIAANJBPBIJBDIDDCCM; Ecp_IpLoginFail=22101758.212.197.250; ASPSESSIONIDSCQDTQTA=GIKMHACCABAJAAIOCEMOEMHK; CNZZDATA1279462118=620665052-1650760587-%7C1665995467; dperpage=50; dblang=ch; knsLeftGroupSelectItem=1%3B2%3B; CurrSortField=Publication+Date%2f(%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2c%27TIME%27); CurrSortFieldType=desc',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }

    def start_requests(self):
        abs_path = r'F:\CNKI主站\中图分类号\file_em\file_in\\'
        # file_names = os.listdir(abs_path)
        file_names = ['A8 马克思主义、列宁主义、毛泽东思想、邓小平理论的学习和研究.csv', 'B84 心理学.csv', 'C91 社会学.csv', 'C93 管理学.csv', 'C95 民族学.csv', 'D631 公安工作.csv', 'D9 法律.csv', 'D917 犯罪学.csv', 'D918 刑事侦查学（犯罪对策学、犯罪侦查学）.csv', 'E22 政治工作.csv', 'E251 军事教育、军事训练.csv', 'E29 军事史（战史、建军史）.csv', 'F3 农业经济.csv', 'F323.2 农业资源开发与利用.csv', 'F326.2 林业.csv', 'G2 信息与知识传播.csv', 'G250 图书馆学.csv', 'G27 档案学、档案事业.csv', 'G35 情报学、情报工作.csv', 'G4 教育.csv', 'G8 体育.csv', 'H1 汉语.csv', 'H3 常用外国语.csv', 'I2 中国文学.csv', 'J 艺术.csv', 'J0 艺术理论.csv', 'J6 音乐.csv', 'J8 戏剧艺术.csv', 'J9 电影、电视艺术.csv', 'K092 中国.csv', 'K1 世界史.csv', 'K2 中国史.csv', 'K9 地理.csv', 'O1 数学.csv', 'O3 力学.csv', 'O4 物理学.csv', 'O43 光学.csv', 'O6 化学.csv', 'O7 晶体学.csv', 'P1 天文学.csv', 'P2 测绘学.csv', 'P3 地球物理学.csv', 'P4 大气科学（气象学）.csv', 'P5 地质学.csv', 'P61 矿床学.csv', 'P62 地质、矿产普查与勘探.csv', 'P7 海洋学.csv', 'P75 海洋工程.csv', 'P9 自然地理学.csv', 'Q 生物科学.csv', 'Q81 生物工程学（生物技术）.csv', 'R1 预防医学、卫生学.csv', 'R2 中国医学.csv', 'R28 中药学.csv', 'R3 基础医学.csv', 'R318 生物医学工程.csv', 'R4 临床医学.csv', 'R47 护理学.csv', 'R6 外科学.csv', 'R71 妇产科学.csv', 'R72 儿科学.csv', 'R74 神经病学与精神病学.csv', 'R75 皮肤病学与性病学.csv', 'R77 眼科学.csv', 'R78 口腔科学.csv', 'R8 特种医学.csv', 'R9 药学.csv', 'S157 水土保持.csv', 'S2 农业工程.csv', 'S4 植物保护.csv', 'S5 农作物.csv', 'S54 饲料作物、牧草.csv', 'S6 园艺.csv', 'S68 观赏园艺（花卉和观赏树木）.csv', 'S7 林业.csv', 'S8 畜牧、动物医学、狩猎、蚕、蜂.csv', 'S85 动物医学（兽医学）.csv', 'S9 水产、渔业.csv', 'TB472 产品设计.csv', 'TB6 制冷工程.csv', 'TD 矿业工程.csv', 'TD1 矿山地质与测量.csv', 'TE 石油、天然气工业.csv', 'TF 冶金工业.csv', 'TH 机械、仪表工业.csv', 'TK 能源与动力工程.csv', 'TL 原子能技术.csv', 'TM 电工技术.csv', 'TN 无线电电子学、电信技术.csv', 'TN4 微电子学、集成电路（IC）.csv', 'TN91 通信.csv', 'TP13 自动控制理论.csv', 'TP273 自动控制、自动控制系统.csv', 'TP3 计算技术、计算机技术.csv', 'TP311.5 软件工程.csv', 'TQ 化学工业.csv', 'TQ92 发酵工业.csv', 'TS1 纺织工业、染整工业.csv', 'TS2 食品工业.csv', 'TS5 皮革工业.csv', 'TS7 造纸工业.csv', 'TS941 服装工业.csv', 'TU 建筑科学.csv', 'TU98 区域规划、城乡规划.csv', 'TU986 园林规划与建设.csv', 'TV 水利工程.csv', 'U 交通运输.csv', 'U66 船舶工程.csv', 'X1 环境科学基础理论.csv', 'X171.4 生态建设与生态恢复.csv', 'X2 社会与环境.csv', 'X3 环境保护管理.csv', 'X32 环境规划与环境管理.csv', 'X5 环境污染及其防治.csv', 'X7 废物处理与综合利用.csv', 'X8 环境质量评价与环境监测.csv', 'X93 安全工程.csv']
        # 85:89
        for one_file in file_names[110:112]:
            print(one_file)
            pf = pd.read_csv(abs_path + one_file, dtype=str)
            sha = pf.shape[0]
            meta = dict(path=abs_path, name=one_file.strip('.csv'))
            for i in range(0, sha):
                url = pf.values[i][2]
                yield ReSpider.Request(
                    url=url,
                    headers=self.headers,
                    meta=meta,
                    proxy='http://127.0.0.1:1080'
                )

    def parse(self, response):
        meta = response.meta
        html = response.text
        if "文件不存在" not in html:
            res = etree.HTML(html)
            title_name = res.xpath('//div[@class="wx-tit"]/h1/text()')[0] if res.xpath(
                '//div[@class="wx-tit"]/h1/text()') else ''
            author = res.xpath('//div[@class="wx-tit"]/h3/span/text()')
            author = ''.join(author)
            abstract = res.xpath('//*[@id="ChDivSummary"]//text()')
            abstract = ''.join(abstract)

            keywords = res.xpath('//p[@class="keywords"]/a/text()')  # 关键词
            keywords = [i.replace('\n', '').replace(' ', '') for i in keywords]
            keywords = ''.join(keywords)
            fund = res.xpath('//p[@class="funds"]/a/text()')
            fund = [i.replace('\n', '').replace(' ', '') for i in fund]
            fund = ';'.join(fund)
            doi = res.xpath('//li[@class="top-space"]/span[contains(text(), "DOI：")]/parent::li/p/text()')
            doi = ';'.join(doi)
            series = res.xpath('//li[@class="top-space"]/span[contains(text(), "Series：")]/parent::li/p/text()')
            series = ';'.join(series)
            subject = res.xpath('//li[@class="top-space"]/span[contains(text(), "Subject：")]/parent::li/p/text()')
            subject = ';'.join(subject)
            clc = res.xpath(
                '//li[@class="top-space"]/span[contains(text(), "Classification Code：")]/parent::li/p/text()')
            clc = ';'.join(clc)

            journal_name = res.xpath('//div[@class="top-tip"]/span//text()')
            journal_name = [i.replace('\n', '').replace(' ', '') for i in journal_name]
            journal_name = ';'.join(journal_name)

            data_list = item.CSVListItem(data_directory=r'F:\my_workfiles\CNKI\CLC\file_in', filename=f'{meta["name"]}')
            data_list.append(
                dict(title_name=title_name, author=author, abstract=abstract, keywords=keywords, fund=fund, doi=doi,
                     series=series, subject=subject, clc=clc, journal_name=journal_name))
            yield data_list


if __name__ == '__main__':
    ClcDown().start()
