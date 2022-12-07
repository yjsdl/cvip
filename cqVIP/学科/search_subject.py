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
from copy import deepcopy


class QikanQuerySearch(ReSpider.Spider):
    __custom_setting__ = {
        'TASK_LIMIT': 1,
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
    # table_head = ['摘要']
    data_save_path = 'E:/数据科学平台'

    def start_requests(self):
        pf = pd.read_csv('./学科统计.csv', dtype=str)['name'].values.tolist()
        pf = ['哲学', '马克思主义哲学', '中国哲学', '外国哲学', '逻辑学', '伦理学', '美学', '宗教学', '科学技术哲学', '经济学', '理论经济学', '政治经济学', '经济思想史', '经济史',
     '西方经济学', '世界经济', '人口、资源与环境经济学', '应用经济学', '国民经济学', '区域经济学', '财政学', '金融学', '产业经济学', '国际贸易学', '劳动经济学', '统计学', '数量经济学',
     '国防经济',  '法学理论', '法律史', '宪法学与行政法学', '刑法学', '民商法学', '诉讼法学', '经济法学', '环境与资源保护法学', '国际法学', '军事法学', '政治学',
     '政治学理论', '中外政治制度', '科学社会主义与国际共产主义运动', '国际政治', '国际关系', '外交学', '社会学', '人口学', '人类学', '民俗学', '民族学',
     '马克思主义民族理论与政策', '中国少数民族经济', '中国少数民族史', '中国少数民族艺术', '马克思主义理论', '马克思主义基本原理', '马克思主义发展史', '马克思主义中国化研究', '国外马克思主义研究',
     '思想政治教育', '中国近现代史基本问题研究', '公安学', '公安学基础理论', '公安管理学', '治安学', '侦查学', '犯罪学', '公安情报学', '国内安全保卫学', '边防管理学', '涉外警务学',
     '警务指挥与战术', '警卫学', '教育学', '教育学原理', '课程与教学论', '教育史', '比较教育学', '学前教育学', '高等教育学', '成人教育学', '职业技术教育学', '特殊教育学', '教育技术学',
     '心理学', '基础心理学', '发展与教育心理学', '应用心理学', '体育学', '体育人文社会学', '运动人体科学', '体育教育训练学', '民族传统体育学', '文学', '中国语言文学', '文艺学',
     '语言学及应用语言学', '汉语言文字学','中国古代文学', '中国现当代文学', '中国少数民族语言文学', '比较文学与世界文学', '外国语言文学', '英语语言文学', '俄语语言文学',
     '法语语言文学', '德语语言文学', '日语语言文学', '印度语言文学', '西班牙语语言文学', '阿拉伯语语言文学', '欧洲语言文学', '亚非语言文学', '外国语言学及应用语言学', '新闻传播学', '新闻学',
     '传播学', '历史学', '考古学', '考古学史和考古学理论', '史前考古', '夏商周考古', '秦汉魏晋南北朝考古', '唐宋元明清考古', '科技考古', '文化遗产与博物馆', '古代文字与铭刻', '专门考古',
     '中国史', '历史地理学', '历史文献学', '史学理论及中国史学史', '中国古代史', '中国近代史', '中国现代史', '专门史', '世界史', '世界史学理论与史学史', '世界古代中古史', '世界近现代史',
     '世界地区 国别史', '专门史与整体史', '理学', '数学', '基础数学', '计算数学', '概率论与数理统计', '应用数学', '运筹学与控制论', '物理学', '理论物理', '粒子物理与原子核物理',
     '原子与分子物理', '等离子体物理', '凝聚态物理', '声学', '光学', '无线电物理', '化学', '无机化学', '分析化学', '有机化学', '物理化学', '高分子化学与物理', '天文学', '天体物理',
     '天体测量与天体力学', '地理学', '自然地理学', '人文地理学', '地图学与地理信息系统', '气象学', '大气物理学与大气环境', '海洋科学', '物理海洋学', '海洋化学', '海洋生物学',
     '海洋地质', '地球物理学', '固体地球物理学', '空间物理学', '地质学', '矿物学、岩石学、矿床学', '地球化学', '古生物学与地层学', '构造地质学', '第四纪地质学', '生物学', '植物学',
     '动物学', '生理学', '水生生物学', '微生物学', '神经生物学', '遗传学', '发育生物学', '细胞生物学', '生物化学与分子生物学', '生物物理学', '系统科学', '系统理论', '系统分析与集成',
     '科学技术史', '生态学', '工学', '力学', '一般力学与力学基础', '固体力学', '流体力学', '工程力学', '机械工程', '机械制造及其自动化', '机械电子工程', '机械设计及理论',
     '光学工程', '仪器科学与技术', '精密仪器及机械', '测试计量技术及仪器', '材料科学与工程', '材料物理与化学', '材料学', '材料加工工程', '冶金工程', '冶金物理化学', '钢铁冶金',
     '有色金属冶金', '动力工程及工程热物理', '热能工程', '动力机械及工程', '流体机械及工程', '化工过程机械', '电气工程', '电机与电器', '电力系统及其自动化',
     '高电压与绝缘技术', '电力电子与电力传动', '电工理论与新技术', '电子科学与技术', '物理电子学', '电路与系统', '微电子学与固体电子学', '电磁场与微波技术', '信息与通信工程', '通信与信息系统',
     '信号与信息处理', '控制科学与工程',  '检测技术与自动化装置', '系统工程', '模式识别与智能系统', '导航、制导与控制', '计算机科学与技术', '计算机系统结构',
     '计算机软件与理论', '计算机应用技术', '建筑学', '建筑历史与理论', '建筑设计及其理论', '城市规划与设计', '土木工程', '岩土工程', '结构工程', '市政工程',
     '供热、供燃气、通风及空调工程', '防灾减灾工程及防护工程', '桥梁与隧道工程', '水利工程', '水文学及水资源', '水力学及河流动力学', '水工结构工程', '水利水电工程', '港口、海岸及近海工程',
     '测绘科学与技术', '大地测量学与测量工程', '摄影测量与遥感', '地图制图学与地理信息工程', '化学工程与技术', '化学工程', '化学工艺', '生物化工', '应用化学', '工业催化', '地质资源与地质工程',
     '矿产普查与勘探', '地球探测与信息技术', '地质工程', '矿业工程', '采矿工程', '矿物加工工程', '安全技术及工程', '石油与天然气工程', '油气井工程', '油气田开发工程', '油气储运工程',
     '纺织科学与工程', '纺织工程', '纺织材料与纺织品设计', '纺织化学与染整工程', '服装设计与工程', '轻工技术与工程', '制浆造纸工程', '制糖工程', '发酵工程', '皮革化学与工程', '交通运输工程',
     '道路与铁道工程', '交通信息工程及控制', '交通运输规划与管理', '载运工具运用工程', '船舶与海洋工程', '船舶与海洋结构物设计制造', '轮机工程', '水声工程', '航空宇航科学与技术', '飞行器设计',
     '航空宇航推进理论与工程', '航空宇航制造工程', '人机与环境工程', '兵器科学与技术', '武器系统与运用工程', '兵器发射理论与技术', '火炮、自动武器与弹药工程', '军事化学与烟火技术', '核科学与技术',
     '核能科学与工程', '核燃料循环与材料', '核技术及应用', '辐射防护及环境保护', '农业工程', '农业机械化工程', '农业水土工程', '农业生物环境与能源工程', '农业电气化与自动化', '林业工程',
     '森林工程', '木材科学与技术', '林产化学加工工程', '环境科学与工程', '环境科学', '环境工程', '生物医学工程', '食品科学与工程', '食品科学', '粮食、油脂及植物蛋白工程',
     '农产品加工及贮藏工程', '水产品加工及贮藏工程', '城乡规划学', '区域发展与规划', '城乡规划与设计', '住房与社区建设规划', '城乡发展历史与遗产保护规划', '城乡生态环境与基础设施规划', '城乡规划管理',
     '风景园林学', '软件工程', '生物工程', '安全科学与工程', '公安技术', '网络空间安全', '农学', '作物学', '作物栽培学与耕作学', '作物遗传育种', '园艺学', '果树学', '蔬菜学',
     '茶学', '农业资源与环境', '土壤学', '植物营养学', '植物保护', '植物病理学', '农业昆虫与害虫防治', '农药学', '畜牧学', '动物遗传育种与繁殖', '动物营养与饲料科学', '草业科学',
     '特种经济动物饲养', '兽医学', '基础兽医学', '预防兽医学', '临床兽医学', '林学', '林木遗传育种', '森林培育', '森林保护学', '森林经理学', '野生动植物保护与利用', '园林植物与观赏园艺',
     '水土保持与荒漠化防治', '水产', '水产养殖', '捕捞学', '渔业资源', '草学', '医学', '基础医学', '人体解剖与组织胚胎学', '免疫学', '病原生物学', '病理学与病理生理学', '法医学',
     '放射医学', '航空、航天与航海医学', '临床医学', '内科学', '儿科学', '老年医学', '神经病学', '精神病与精神卫生学', '皮肤病与性病学', '影像医学与核医学', '临床检验诊断学', '护理学',
     '外科学', '妇产科学', '眼科学', '耳鼻咽喉科学', '肿瘤学', '康复医学与理疗学', '运动医学', '麻醉学', '急诊医学', '口腔医学', '口腔基础医学', '口腔临床医学', '公共卫生与预防医学',
     '流行病与卫生统计学', '劳动卫生与环境卫生学', '营养与食品卫生学', '儿少卫生与妇幼保健学', '卫生毒理学', '军事预防医学', '中医学', '中医基础理论', '中医临床基础', '中医医史文献', '方剂学',
     '中医诊断学', '中医内科学', '中医外科学', '中医骨伤科学', '中医妇科学', '中医儿科学', '中医五官科学', '针灸推拿学', '民族医学', '中西医结合', '中西医结合基础', '中西医结合临床',
     '药学', '药物化学', '药剂学', '生药学', '药物分析学', '微生物与生化药学', '药理学', '中药学', '特种医学', '医学技术', '军事学', '军事思想及军事历史', '军事思想', '军事历史',
     '战略学', '军事战略学', '战争动员学', '战役学', '联合战役学', '军种战役学', '战术学', '合同战术学', '兵种战术学', '作战指挥学', '军事运筹学', '军事通信学',
     '军事情报学', '密码学', '军事教育训练学', '军事管理学', '军事组织编制学', '军队管理学', '军队政治工作学', '军事后勤学与军事装备学', '军事后勤学', '后方专业勤务', '军事装备学',
     '军事训练学', '管理学', '管理科学与工程', '工商管理', '会计学', '企业管理', '旅游管理', '技术经济及管理', '农林经济管理', '农业经济管理', '林业经济管理', '公共管理', '行政管理',
     '社会医学与卫生事业管理', '教育经济与管理', '社会保障', '土地资源管理', '图书情报与档案管理', '图书馆学', '情报学', '档案学', '艺术学', '艺术学理论', '音乐与舞蹈学', '戏剧与影视学',
     '美术学', '设计学', '交叉学科', '集成电路科学与工程', '国家安全学']
        # sha = pf.shape[0]
        # for i in pf[0:1]:
        i = '哲学'
        for j in range(1, 2):
            issn_name = i
            param = dict(field='任意字段', search_key=issn_name, page_num=j, page_size=100)
            yield ReSpider.Request(
                url='http://qikan.cqvip.com/Search/SearchList',
                method='POST',
                data=self.searchParam(field='任意字段', search_key=issn_name, page_num=j, page_size=100),
                retry=True,
                meta=param,
            )

    def parse(self, response):
        meta = response.meta
        print(meta)

        # # 导出逻辑
        # ids = []
        # row_nodes = response.xpath('//*[@id="remark"]/dl')
        # for row_node in row_nodes:
        #     ids.append(row_node.xpath('./dt[1]/a/@articleid').get())
        # yield ReSpider.Request(
        #     url=self.export_excel,
        #     method='POST',
        #     data={'filename': '',
        #           'content': json.dumps({"ids": ','.join(ids)}, ensure_ascii=False)},
        #     meta=meta,
        #     callback=self.export_parse
        # )
        # 新任务逻辑
        # if meta.get('MAX_PAGE') is None:
        #     # 翻页逻辑
        #     total_count = response.xpath('//input[@id="hidShowTotalCount"]/@value').get()
        #     total_count = int(total_count)
        #     self.logger.info(
        #         '%s  %s 找到 %s 篇文章' % (
        #             meta['search_key'], meta.get('cluster_filter', ''),
        #             total_count))
        #     meta['MAX_PAGE'] = math.ceil(total_count / 100)
        #     if meta['MAX_PAGE'] > 15:
        #         meta['MAX_PAGE'] = 15
        #
        #     for p in range(2, meta['MAX_PAGE'] + 1):
        #         meta_copy = deepcopy(meta)
        #         meta_copy['page_num'] = p
        #         searchParamModel = SearchParamModel(**meta_copy)
        #         yield ReSpider.Request(
        #             url='http://qikan.cqvip.com/Search/SearchList',
        #             method='POST',
        #             data={'searchParamModel': searchParamModel()},
        #             retry=True,
        #             meta=meta
        #         )

    def searchParam(self,
                    field: str = '任意字段',  # 搜索字段
                    search_key: str = None,  # 搜索词
                    start_year: int = '', end_year: int = '',
                    page_num: int = 1, page_size: int = 20,
                    **kwargs):
        if search_key is None:
            raise ValueError("search_key 不能为空")
        show_rules = f"  {field}={search_key}  "
        adv_show_title = field + '=' + search_key

        searchParamModel = {"ObjectType": 1, "SearchKeyList": [
            {"FieldIdentifier": "U", "SearchKey": search_key, "PreLogicalOperator": "", "AfterLogicalOperator": None,
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
        # with open('./test.xls', 'wb') as f:
        #     f.write(response.content)

        rows = re.findall(r'<Row ss:AutoFitHeight=\'1\'>(.*?)</Row>', response.text)
        # data_list = item.CSVListItem(data_directory=f'{self.data_save_path}/{meta["search_key"]}/',
        #                              filename=f'{meta["search_key"]}{meta["start_year"]}-{meta["end_year"]}中文发文')

        data_list = item.CSVListItem(data_directory=fr'F:/维普/学科/{meta.get("search_key")}', filename=rf'{meta["page_num"]}')
        # data_list = item.MysqlListItem(table='data_cqvip_post')
        for row in rows:
            items = re.findall(r'<Data ss:Type=\'String\'>(.*?)</Data>', row)
            data_list.append(dict(zip(self.table_head, items)))
        yield data_list


if __name__ == '__main__':
    QikanQuerySearch().start()
