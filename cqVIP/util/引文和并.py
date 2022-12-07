import pandas as pd


def func(filename: str):
    refId_df = pd.read_csv(root + filename)
    # refId_df.dropna(inplace=True)
    refId_df.drop_duplicates(keep='first', inplace=True)
    group_obj = refId_df.groupby(by=['aid'])
    save_list = []
    for k, v in group_obj:
        print(k)
        try:
            dict1 = {'FileName': str(k), 'Reference': '; '.join(list(v['yinwen'])), 'byl': list(v['byl'])[0]}
            # print(dict1)
        except TypeError:
            print(k, ': ', list(v['yinwen']))
            break
        else:
            save_list.append(dict1)
        # dict1 = {'FileName': str(k), 'Reference': '; '.join(list(v['reference']))}
        # print(dict1)
        # save_list.append(dict1)
    df = pd.DataFrame(save_list, columns=['FileName', 'Reference', 'byl'])

    print(df)
    REFERENCE = filename.replace('.csv', '_引文.csv')
    print(REFERENCE)
    df.to_csv(root+REFERENCE, index=False)


def hebing(filename, refernce):
    ftype = filename[filename.index('.'):]
    left = pd.read_csv(root+filename) if '.csv' in filename.lower() else pd.read_excel(root+filename, engine='openpyxl')
    right = pd.read_csv(root+refernce)[['FileName', 'Reference', 'byl']]
    left['aid'] = left['网址'].str.split('=', expand=True)[1]
    # print(left)
    df = pd.merge(left, right, how='left', left_on=['aid'], right_on=['FileName'])
    # print(df)
    df.rename(columns={'Reference': '引文', 'byl': '被引量'}, inplace=True)
    print(df)
    new_columns = [c.strip().replace(' ', '').replace('\u3000', '') for c in df.columns.values.tolist()]
    # print(new_columns)
    df.columns = new_columns
    # df.to_csv(root + filename.replace(ftype, '含引用.csv'), index=False)
    df.to_excel(root + filename.replace(ftype, '含引用.xlsx'), index=False, engine='xlsxwriter')


def split_df():
    df =pd.read_csv(root+'四川大学.csv')
    group = df.groupby(by=['年'])
    for k, v in group:
        v.to_csv(root+'/年/'+'四川大学.csv'.replace('.csv', f'{k}年.csv'), index=False)


if __name__ == '__main__':
    root = r'F:\工作数据存储2022\20220421_cssci更新\华中农业大学/'
    # root = 'F:/工作数据存储2022/20220301_ers数据更新/'
    # REFERENCE = 'data_weipu_scdx2021'
    REFERENCE = 'data_weipu_cscd'
    # func(f'{REFERENCE}.csv')
    # print(REFERENCE)
    hebing('华中农业大学2022cscd.csv', f'{REFERENCE}_引文.csv')
    print('处理完成.')
