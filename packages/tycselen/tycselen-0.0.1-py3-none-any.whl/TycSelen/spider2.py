#coding=utf-8

import os
import re
import xlsxwriter
from datetime import datetime
from pymongo import MongoClient
import pandas as pd
import numpy as np
import json
import pandas as pd


rootPath=r'./'

class Mongo():
    #初始化
    def __init__(self,stamp=None):
        self.stamp = (datetime.now()).strftime('%Y%m%d') if stamp is None else stamp
        self.client = MongoClient("localhost", 27017)
        self.db=self.client['tianyancha']
        self.db2 = self.client['tianyancha']

    # excel汇总去重
    def huizong(self, dirpath):
        df_out = None
        self._matches = self.db2['df_qichacha']
        print('Waiting...')
        print(len(os.listdir(dirpath)))
        index=0
        for filename in os.listdir(dirpath):
            index+=1
            filepath = os.path.join(dirpath, filename).replace('\\', '/')
            print(index, filepath)
            # data = pd.read_excel(filepath, header=0, skiprows=1, nrows=1)
            df_in = pd.read_excel(filepath, header=1)
            print(df_in)
            df_value = json.loads(df_in.T.to_json()).values()
            self._matches.insert_many(df_value)

        print('去重')
        # df_out.drop_duplicates(subset=['mid'], keep='first', inplace=True)
        # df_out.to_excel('search_汇总.xlsx', engine='xlsxwriter')

    # pd导入
    def pb_import(self):
        self._matches = self.db2['df_qichaccha']
        df=pd.read_excel(r'search_汇总3.xlsx')
        df_value=json.loads(df.T.to_json()).values()
        # print(df_value)
        self._matches.insert_many(df_value)

    # pd导出
    def pb_export(self):
        table_name = 'search_qichacha'
        self._matches = self.db2[table_name]
        # matches = self._matches.find()
        matches = self._matches.find({'匹配状态': 0})
        df = pd.DataFrame(list(matches))
        del df['_id']
        # df=df[['symbol', '匹配名称']]
        print(df)
        df.to_excel('pd_out.xlsx')

    # df求交集，差集，出结果
    def pb_export2(self):
        try:
            table_name = 'df_qichacha'
            self._matches = self.db2[table_name]
            matches = self._matches.find()
            df1 = pd.DataFrame(list(matches))
            del df1['_id']
            df1 = df1[['企业名称', '成立日期', '所属省份', '纳税人识别号', '企业类型', '所属行业', '企业地址']]
            # df1 = pd.read_excel('input3.xlsx')
            # df1 = df1[['企业名称']]
            print(df1)
            df2=pd.read_excel('匹配2.xlsx')
            df2 = df2[['公司名称', '匹配名称']]
            print(df2)
            # 合集
            df=pd.merge(df2, df1, left_on='匹配名称', right_on='企业名称', how='left')
            df.drop_duplicates(subset=['公司名称'], keep='first', inplace=True)
            print(df)
            # 交集（完全匹配的）
            df = df.loc[df['企业名称'].str.len().gt(0)]
            # 差集（未完全匹配的）
            # df = df.loc[df['企业名称'].isnull()]


            df.reset_index(drop=True, inplace=True)
            print(df)
            df.to_excel('合并2.xlsx')

        except Exception as e:
            print (e)

    # 预处理待查询公司名单
    def pb_export3(self):
        try:
            df=pd.read_excel('input2.xlsx')
            for index, row in df.iterrows():
                print(row)
                try:
                    # print(df.iloc[index, 0])
                    df.iloc[index, 0] = row[0].replace('(', '（').replace(')', '）')
                except Exception as e:
                    print(e)
            # df.drop_duplicates(subset=['企业名称'], keep='first', inplace=True)
            df.to_excel('input3.xlsx')

        except Exception as e:
            print(e)

    # df求交集，差集，出结果
    def pb_export4(self):
        try:
            df1 = pd.read_excel('模糊匹配.xlsx')
            df1 = df1[['公司名称', '企业名称']]
            print(df1)
            df2=pd.read_excel('匹配2.xlsx')
            df2 = df2['公司名称']
            print(df2)
            # 合集
            df=pd.merge(df1, df2, left_on='公司名称', right_on='公司名称', how='right')
            df.drop_duplicates(subset=['公司名称'], keep='first', inplace=True)
            print(df)
            # 交集（完全匹配的）
            # df = df.loc[df['企业名称'].str.len().gt(0)]
            # 差集（未完全匹配的）
            df = df.loc[df['企业名称'].isnull()]


            # df.reset_index(drop=True, inplace=True)
            print(df)
            df.to_excel('合并2.xlsx')

        except Exception as e:
            print (e)

    # search求交集，差集，出待查名单
    def pb_export5(self):
        try:
            table_name = 'search_qichacha'
            self._matches = self.db2[table_name]
            # matches = self._matches.find()
            matches = self._matches.find({'匹配状态': 1})
            df1 = pd.DataFrame(list(matches))
            # del df1['_id']
            df1=df1[['symbol', '匹配名称']]
            print(df1)
            df2=pd.read_excel('待查询.xlsx')
            df2 = df2['公司名称']
            print(df2)
            # 合集
            df=pd.merge(df2, df1, left_on='公司名称', right_on='symbol', how='left')
            df.drop_duplicates(subset=['symbol'], keep='first', inplace=True)
            print(df)
            # 交集（完全匹配的）
            df = df.loc[df['symbol'].str.len().gt(0)]
            # 差集（未完全匹配的）
            # df = df.loc[df['企业名称'].isnull()]


            df.reset_index(drop=True, inplace=True)
            print(df)
            df.to_excel('合并2.xlsx')

        except Exception as e:
            print (e)
            quit()




# 主程序入口
if __name__ == '__main__':
    # Ctrl+ / 切换注释
    db = Mongo()
    db.pb_export()
    # db.pb_import()

    print('\nTS:'+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))



