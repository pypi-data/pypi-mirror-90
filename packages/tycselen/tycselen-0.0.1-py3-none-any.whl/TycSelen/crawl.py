# -*- coding:utf-8 -*-


import re
import json
import requests
from bs4 import BeautifulSoup
from TycSelen import info
from pymongo import MongoClient
import time
import random
import datetime
import xlsxwriter
from urllib import parse
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TycSelen():

    def __init__(self):
        self.urls = {}                      # 目标网页
        self.headers = {}                   # Get/Post请求头
        self.param = {}
        self.cookie=requests.cookies.RequestsCookieJar()
        self.session = requests.session()
        self.client = MongoClient("localhost", 27017)
        self.db=self.client['tianyancha']
        self.keyword=None
        self.df_search=None
        self.df_detail=None
        self.status_code=None
        self.wait=1


    # 从配置文件中更新登录链接信息
    def update_info(self):
        self.urls = info.loginUrls
        self.headers = info.loginHeaders
        self.param = info.loginParam
        self.cookie.set("cookie", info.loginCookie)
        self.session.cookies.update(self.cookie)

    # 从配置文件中更新登录链接信息
    def selen_init(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9996")
        # chrome_options.add_argument('--headless')
        chrome_driver = "C:\Program Files\Google\Chrome\Application/chromedriver.exe"
        # self.browser = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
        self.browser = webdriver.Chrome(chrome_driver, options=chrome_options)


    # 发送Get请求
    def requests_get(self, url, param=None, headers=None):
        try:
            url = url if param is None else url+parse.urlencode(param)
            time.sleep(random.random() * 5 + 1)  # 0-1区间随机数
            #没有缓存就开始抓取
            print(json.dumps(self.urls['proxies']) + ' --> ' + url)
            # response = self.session.get(url, proxies=self.urls['proxies'], headers=headers, verify=False)
            # self.session.keep_alive = False
            response = requests.get(url, headers=headers, timeout=10, verify=False)
            response.encoding = response.apparent_encoding
            self.status_code=response.status_code
            value = response if response.status_code == requests.codes.ok else None
        except Exception as e:
            value = None
        finally:
            return value

    # 发送Get请求
    def selen_get(self, url, param=None):
        try:
            url = url if param is None else url+parse.urlencode(param)
            print(url)
            time.sleep(random.random() * self.wait + 1)  # 0-1区间随机数
            self.status_code = self.browser.get(url)
            value = self.browser.page_source
        except Exception as e:
            value = None
        finally:
            return value

    # 搜索新闻
    def search_enterprires(self, keyword, day=-365*50, pn=None):
        self.keyword = keyword
        result=None
        try:
            self.df_search = pd.DataFrame(columns=['company', 'url', 'state', 'taglist', 'inforow', 'contactrow', 'matchrow'])
            # self.df_search.set_index('company')
            self.param['home']['key']=self.keyword

            self.enterprire_parse(keyword, day=day, pn=pn)

            result=self.df_search

        except Exception as e:
            print(e)
        finally:
            return result

    # 搜索新闻
    def enterprire_parse(self, keyword, day=-365*50, pn=None):
        result=None
        try:
            response = self.selen_get(self.urls['home'], self.param['home'])

            soup = BeautifulSoup(response, "html.parser")
            search_block = soup.find('div', attrs={'class': 'search-block header-block-container'})
            if search_block is None:
                self.status_code=-1
                # print('查询失败，请检查确认验证码')
                return
            else:
                self.status_code = -2
            result_list = search_block.find('div', attrs={'class': 'result-list sv-search-container'})
            if result_list is None:
                # print('no search result')
                return
            search_results=result_list.find_all('div',attrs={'class': 'search-item sv-search-company'})
            # print(len(search_results))
            for item in search_results:
                try:
                    content = item.find('div', class_='content')
                    # 名称，网址，经营状态
                    header = content.find('div', class_='header')
                    name = header.a.text.strip()
                    url = header.a['href']
                    state = header.div.text.strip() if header.div is not None else None
                    # 企业标签
                    taglist = content.find('div', class_='tag-list')
                    tags=[x.text for x in taglist.find_all('div')] if taglist is not None else []
                    # 基本信息
                    inforow = content.find('div', class_='info row text-ellipsis')
                    infos = [x.text for x in inforow.find_all('div')] if inforow is not None else []
                    infos = dict(zip([x.split('：')[0].strip() for x in infos], [x.split('：')[1].strip() for x in infos]))
                    # 电话、地址联系方式
                    contactrows = content.find_all('div', class_='contact row')
                    contacts =[]
                    for contact in contactrows:
                        for x in contact.find_all('div'):
                            contacts.append(x.text.strip())
                    contacts = dict(zip([x.split('：')[0].strip() for x in contacts], [x.split('：')[1].strip() for x in contacts]))
                    # 本次查询匹配信息
                    matchrow = content.find('div', class_='match row mult-match-fileid-wrap -qa')
                    matchs = [x.text for x in matchrow.find_all('div')] if matchrow is not None else []
                    matchs = dict(zip([x.split('：')[0].strip() for x in matchs], [x.split('：')[1].strip() for x in matchs]))

                    row=[name, url, state, tags, infos, contacts, matchs]
                    # print(row)
                    self.df_search.loc[len(self.df_search)] = row
                except Exception as e:
                    print(e)
                    continue

        except Exception as e:
            print(e)
        finally:
            return result

    def start(self, filename, rowindex=0):
        self.update_info()
        self.selen_init()

        df_excel=pd.read_excel(filename, dtype=object)
        try:
            for index, excel_row in df_excel.iterrows():
                print(index)
                if index < rowindex:
                    continue
                if index > 50:
                    break
                try:
                    name = excel_row['公司名称'].replace('(', '（').replace(')', '）')
                    print(name)
                    state = excel_row['匹配状态']
                    flag = False if state in [0, 1, 2] else True
                    if flag:  # 逐条操作数据库比较耗时；暂时关闭
                        # if flag or match['匹配名称']=='NaN':  # 逐条操作数据库比较耗时；暂时关闭
                        df_search = self.search_enterprires(name)
                        print(df_search)
                        if self.status_code == -1:
                            print('网页请求失败退出，请检查处理验证码')
                            break
                        # companies = list(zip([x for x in df_search['company']],[x for x in df_search['url']]))
                        companies = df_search.T.to_json(force_ascii=False)
                        excel_row['查询结果'] = companies
                        # excel_row['匹配名称'] = 'NaN'
                        if len(df_search) > 0:
                            # df_match = df_search.loc[df_search['company'] == name]
                            df_match = df_search.loc[df_search['matchrow'].str.contains(name.upper(), na=False)]
                            if not df_match.empty:
                                match_row = df_match.iloc[0, :]
                                excel_row['匹配状态'] = 2
                            else:
                                match_row = df_search.iloc[0, :]
                                excel_row['匹配状态'] = 1

                            excel_row['匹配名称'] = match_row['company']
                            excel_row['网址'] = match_row['url']
                            excel_row['状态'] = match_row['state']
                            excel_row['标签'] = match_row['taglist']
                            excel_row['基本信息'] = match_row['inforow']
                            excel_row['联系方式'] = match_row['contactrow']
                            excel_row['匹配信息'] = match_row['matchrow']
                        else:
                            excel_row['匹配状态'] = 0
                            excel_row['匹配名称'] = None
                            excel_row['网址'] = None
                            excel_row['状态'] = None
                            excel_row['标签'] = None
                            excel_row['基本信息'] = None
                            excel_row['联系方式'] = None
                            excel_row['匹配信息'] = None

                        df_excel.iloc[index, 0] = excel_row['公司名称']
                        df_excel.iloc[index, 1] = excel_row['查询结果']
                        df_excel.iloc[index, 2] = excel_row['匹配状态']
                        df_excel.iloc[index, 3] = excel_row['匹配名称']
                        df_excel.iloc[index, 4] = excel_row['网址']
                        df_excel.iloc[index, 5] = excel_row['状态']
                        df_excel.iloc[index, 6] = excel_row['标签']
                        df_excel.iloc[index, 7] = excel_row['基本信息']
                        df_excel.iloc[index, 8] = excel_row['联系方式']
                        df_excel.iloc[index, 9] = excel_row['匹配信息']
                        # df_excel.iloc[index, 7] = json.dumps(excel_row['基本信息'], ensure_ascii=False)
                        # df_excel.iloc[index, 8] = json.dumps(excel_row['联系方式'], ensure_ascii=False)
                        # df_excel.iloc[index, 9] = json.dumps(excel_row['匹配信息'], ensure_ascii=False)

                except:
                    continue

        finally:
            print(df_excel)
            df_excel.to_excel(filename, engine='xlsxwriter' ,index=None, encoding='utf-8')


    def test(self):
        self.update_info()
        self.selen_init()
        df_search = self.search_enterprires('CHINA CONSTRUCTION BANK')
        print(df_search)





if __name__ == '__main__':

    ac=TycSelen()
    ac.start('input1.xlsx')
    # ac.start2()
    # ac.test()


