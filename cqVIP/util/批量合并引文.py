# -*- coding: utf-8 -*-
# @Time    : 2021/11/11 14:14
# @Author  : ZhaoXiangPeng
# @File    : 批量合并引文.py

import os
import pandas as pd


class BatchJoin:
    def __init__(self, op=None, sp=None, ft=None, ref=None, *args):
        self.file_tag = ft
        self.reference = ref
        self.open_root = op
        self.save_root = sp or op
        self.reference_content = None

    def merge(self, filename: str):
        refId_df = pd.read_csv(filename)
        # refId_df.dropna(inplace=True)
        group_obj = refId_df.groupby(by=['aid'])
        save_list = []
        for k, v in group_obj:
            # print(k)
            try:
                dict1 = {'FileName': str(k), 'Reference': '; '.join(list(v['yinwen'])), 'byl': list(v['byl'])[0]}
                # print(dict1)
            except TypeError:
                print(k, ': ', list(v['yinwen']))
                break
            else:
                save_list.append(dict1)
        self.reference_content = pd.DataFrame(save_list, columns=['FileName', 'Reference', 'byl'])

        REFERENCE = filename.replace('.csv', '_引文.csv')
        print(REFERENCE)
        self.reference_content.to_csv(REFERENCE, index=False)

    def hebing(self, filename: str):
        print('当前处理: %s' % filename)
        if filename.rsplit('.', maxsplit=1)[-1] == 'csv':
            new_name = filename.rsplit('/', maxsplit=1)[-1].replace('\\', '').replace('.csv', '含引文.xlsx')
        else:
            new_name = filename.rsplit('/', maxsplit=1)[-1].replace('\\', '').replace('.xlsx', '含引文.xlsx')
        left = pd.read_csv(filename) if filename[-4:] == '.csv' else pd.read_excel(filename, engine='openpyxl')
        right = self.reference_content
        left['aid'] = left['网址'].str.split('=', expand=True)[1]
        # print(left)
        df = pd.merge(left, right, how='left', left_on=['aid'], right_on=['FileName'])
        # print(df)
        df.rename(columns={'Reference': '引文', 'byl': '被引量'}, inplace=True)
        print(df)
        new_columns = [c.strip().replace(' ', '').replace('\u3000', '') for c in df.columns.values.tolist()]
        # print(new_columns)
        df.columns = new_columns
        df.to_excel(self.save_root + '../ERS数据更新2022/' + new_name, index=False)

    def get_files(self):
        fs = []
        for x in ['南京审计大学', '三江学院', '中国科学技术大学', '合肥工业大学', '三峡大学', '北京科技大学', '曲阜师范大学', '四川大学', '西安建筑科技大学', '西安电子科技大学', '长安大学']:
            for root, dirs, files in os.walk(self.open_root+x):
                for file in files:
                    # if self.file_tag in file:
                    #     print(root)
                    #     school = root.split('\\')[-1]
                    #     old_name = os.path.join(root, file)
                    #     new_name = old_name.replace('CQVIP'+self.file_tag, school+'.xlsx')
                    #     os.rename(old_name, new_name)
                    #     fs.append(new_name)
                    # else:
                    #     if 'csv' in file.lower():
                    #         continue
                    #     fs.append(os.path.join(root, file))
                    #     fs.append(os.path.join(root, file))
                    if '.xlsx' in file:
                        fs.append(os.path.join(root, file))
        return fs

    def get_files2(self):
        fs = []
        for root, dirs, files in os.walk(self.open_root):
            for file in files:
                # if self.file_tag in file:
                #     print(root)
                #     school = root.split('\\')[-1]
                #     old_name = os.path.join(root, file)
                #     new_name = old_name.replace('CQVIP'+self.file_tag, school+'.xlsx')
                #     os.rename(old_name, new_name)
                #     fs.append(new_name)
                # else:
                #     if 'csv' in file.lower():
                #         continue
                #     fs.append(os.path.join(root, file))
                #     fs.append(os.path.join(root, file))
                if '.csv' in file:
                    fs.append(os.path.join(root, file))
        return fs

    def fail(self):
        big_df = pd.DataFrame()
        for root, dirs, files in os.walk('H:/cqVIP/1更新失败发文'):
            for file in files:
                xlsx = pd.read_excel(os.path.join(root, file), engine='openpyxl')
                big_df = pd.concat([big_df, xlsx])
        fail_df = big_df[big_df['导入结果'] == '失败']
        fail_df.to_csv(self.save_root + '/导入失败.csv', index=False)

    def start(self):
        self.merge(self.reference)
        files = self.get_files2()
        for file in files:
            self.hebing(file)


if __name__ == '__main__':
    bj = BatchJoin(op='F:/工作数据存储2022/20220301_ers数据更新/cqvip2022年/',
                   ft='.csv',
                   ref='F:/工作数据存储2022/20220301_ers数据更新/data_weipu_ers032022.csv')
    print(bj.__dict__)
    # print(bj.get_files())
    bj.start()
    # bj.fail()
