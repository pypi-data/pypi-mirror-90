# -*- coding:utf-8 -*-

import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
from BaiduNews import info
from urllib import parse
import re
import json

import requests
import random


class Spider():

    def __init__(self, stamp=None):
        self.url = 'https://data.stats.gov.cn/search.htm?'
        self.stamp = (datetime.now()).strftime('%Y%m%d') if stamp is None else stamp
        self.client = MongoClient("localhost", 27017)
        # self.client = MongoClient("mongodb://other:nopassword@127.0.0.1/okooo")
        self.db=self.client['weibocrawl']
        self.cookie=requests.cookies.RequestsCookieJar()
        self.session = requests.session()
        self.param={}
        self.urls = {}                      # 目标网页
        self.headers = {}                   # Get/Post请求头

    # 从配置文件中更新登录链接信息
    def update_info(self):
        self.urls = info.loginUrls                                                  #http地址
        self.headers = info.loginHeaders
        self.param = info.loginParam
        self.cookie.set("cookie", info.loginCookie)
        self.session.cookies.update(self.cookie)

    # 发送Get请求
    def requests_get(self, url, data=None):
        try:
            url = url if data is None else url+parse.urlencode(data)
            print(url)
            # url = url.replace('%2C', ',').replace('%3A', ':').replace('%2B', '+')
            # if url in self.cachePool.keys():
            #     print('cache:')
            #     return self.cachePool[url]
            time.sleep(random.random() * 1 + 0.1)  # 0-1区间随机数
            #没有缓存就开始抓取
            response = self.browser.get(url)
            value=self.browser.page_source


            # value = requests.get(url).text
            # value = requests.get(url, verify=False).text
            # print(value)
            # response = self.session.get(url, proxies=self.urls['proxies'], timeout=10)
            # response.encoding = 'utf-8'
            # value = response if response.status_code == requests.codes.ok else None
        except Exception as e:
            print(e)
            value = None
        finally:
            # pass
            return value
    # 保存htmlPage
    # 保存htmlPage
    def write_page(self, path, page):
        f = open(path, 'w')
        f.write(page.encode('utf-8'))
        f.close()
    # 保存htmlPage
    def read_page(self, path):
        with open(path,'r') as f:
            res=f.read()
            print(res)
            return f.read().decode('gbk')

    def headers_eval(self, headers):
        """
        headers 转换为字典
        :param headers: 要转换的 headers
        :return: 转换成为字典的 headers
        """
        try:
            headers = headers.splitlines()  # 将每行独立为一个字符串
            headers = [item.strip() for item in headers if item.strip() and ":" in item]  # 去掉多余的信息 , 比如空行 , 非请求头内容
            headers = [item.split(':') for item in headers]  # 将 key value 分离
            headers = [[item.strip() for item in items] for items in headers]  # 去掉两边的空格
            headers = {items[0]: items[1] for items in headers}  # 粘合为字典
            headers = json.dumps(headers, indent=4, ensure_ascii=False)  # 将这个字典转换为 json 格式 , 主要是输出整齐一点
            print(headers)
        except Exception:
            print("headers eval get error ...")
            headers = dict()

        return headers

    def headers_get(self, get_headers):
        """
        headers 转换为字典
        :param headers: 要转换的 headers
        :return: 转换成为字典的 headers
        """
        try:
            get0=get_headers.split('?')[0]
            print(get0)
            get1 = get_headers.split('?')[1]
            headers = get1.replace('=',':')
            headers = headers.split('&')  # 将每行独立为一个字符串
            headers = [item.strip() for item in headers if item.strip() and ":" in item]  # 去掉多余的信息 , 比如空行 , 非请求头内容
            headers = [item.split(':') for item in headers]  # 将 key value 分离
            headers = [[item.strip() for item in items] for items in headers]  # 去掉两边的空格
            headers = {items[0]: items[1] for items in headers}  # 粘合为字典
            headers = json.dumps(headers, indent=4, ensure_ascii=False)  # 将这个字典转换为 json 格式 , 主要是输出整齐一点
            print(headers)
        except Exception:
            print("headers eval get error ...")
            headers = dict()

        return headers

    # 下载数据并保存
    def pb_repair(self):
        self._matches = self.db['renwumag1980_2']
        try:
            # 不为空查询
            matches = self._matches.find({'is_original': '转载'})
            # matches = self._matches.find({'video_num': {'$gte': 1}})
            for match in matches:
                try:
                    # content_url=match['content_url']
                    # arc_html = self.requests_get(content_url)
                    # match['arc_html']=arc_html

                    if match['key3'] is not None:
                        continue

                    arc_html=match['arc_html']

                    try:
                        # arc_html=match['arc_html']
                        # print(arc_html)
                        # soup_body = BeautifulSoup(arc_html, "html.parser")
                        print('解析')
                        print(match['content_url'])

                        rex = r'来源 \|(.*?)（ID:.*'

                        pos=arc_html.find('来源 |')
                        pos_str=arc_html[pos:pos+200]
                        # print(pos_str)

                        matchObj = re.match(rex, pos_str, re.M | re.I)
                        if matchObj:
                            rex_src=matchObj.group(1).strip().split(';')[-1]
                            match['key3']=rex_src
                            print(rex_src)
                    except:
                        pass


                    self._matches.update_one({'symbol': match['symbol']}, {"$set": match}, True)
                except Exception as e:
                    print(e)
                    continue
            print(matches.count())
        except:
            print (self.stamp + " error, quit()")
            quit()

    def Imatate(self):
        self.update_info()
        # self._matches = self.db['renwumag1980_2']

        # page=requests.get('https://www.amazon.com/Finer-Things-Timeless-Furniture-Textiles/dp/0770434290/ref=lp_4539344011_1_1?s=books&ie=UTF8&qid=1605336684&sr=1-1').text
        # print(page)
        # return

        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9999")
        # chrome_options.add_argument('--headless')
        # selenium 运行时会从系统的环境变量中查找 webdriver.exe
        # 一般把 webdriver.exe 放到 python 目录中，这样就不用在代码中指定。
        chrome_driver = "C:\Program Files\Google\Chrome\Application/chromedriver.exe"
        self.browser = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)

        cookie={
            "rewardsn":"",
            "wxtokenkey": "777",
        }

        # self.browser.add_cookie({'rewardsn':'','wxtokenkey':'777'})

        # self.browser.add_cookie({'name': 'ASP.NET_SessionId', 'value': 'yy3mnikt0zqeolotjahrrkte'})
        # self.browser.add_cookie({'name': 'fvlid', 'value': '1605284317709aRf8bjOAb0'})

        self.browser.get("https://www.creditchina.gov.cn/")
        # print(self.browser.page_source)
        elem=self.browser.find_element_by_id('search_input')
        elem.send_keys("腾讯")

        self.browser.find_element_by_class_name('search_btn').click()
        print(self.browser.page_source)

        # soup=BeautifulSoup(self.browser.page_source, 'lxml')
        # data=json.loads(soup.text)
        # print(data['data'])

        return

        # self.browser = webdriver.PhantomJS()
        # self.browser.implicitly_wait(10)  # 这里设置智能等待10s

        # url = 'https://linwanwan668.taobao.com/i/asynSearch.htm?mid=w-553869820-0&orderType=hotsell_desc'
        url='https://sycm.taobao.com/portal/home.htm?spm=a211vu.server-home.category.d780.4c575e16BTnoaM'


        try:
            # self.crawl3(url)
            self.pb_repair()
        finally:
            # self.browser.close()
            self.client.close()

    # 解析数据
    def export(self):
        try:
            # for record in self._records.find():
            #     self.parse(record['result'])
            #     for betfair in record['betfair']:
            #         self.parse2(betfair)
            page=self.read_page('test.txt')
            print(page)
        except:
            pass

if __name__ == '__main__':

    hear='''
    
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Connection: keep-alive
Cookie: TYCID=aeff78e03ab211eb8c998b95c192d9d8; ssuid=9365707420; _ga=GA1.2.1212525489.1607582475; bad_id658cce70-d9dc-11e9-96c6-833900356dc6=c37e0971-3b58-11eb-999f-c7cdf7fbfc2d; csrfToken=DfVjzGr0dr8QNSwToQREezgY; bannerFlag=true; _utm=e1aad56da76a4dbda9e21218dc42b30b; token=524221acbe6f46bc88dad25625c43230; jsid=SEM-BAIDU-PP-SY-990001; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221764b61cdeaae1-0a78c7c662446b-5a301d45-1327104-1764b61cdebc03%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Fbaidu.php%22%7D%2C%22%24device_id%22%3A%221764b61cdeaae1-0a78c7c662446b-5a301d45-1327104-1764b61cdebc03%22%7D; _gid=GA1.2.3903881.1609755994; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1607653695,1608388941,1609293688,1609755994; RTYCID=749be78f8ade48e8aaf4f3539041250e; CT_TYCID=4e5911635f674ecbb6e6f283c989b42f; cloud_token=cadd4fa168824d9b83636f3f7ef21c88; tyc-user-info={%22claimEditPoint%22:%220%22%2C%22vipToMonth%22:%22false%22%2C%22explainPoint%22:%220%22%2C%22personalClaimType%22:%22none%22%2C%22integrity%22:%2210%25%22%2C%22state%22:%220%22%2C%22score%22:%2245%22%2C%22announcementPoint%22:%220%22%2C%22messageShowRedPoint%22:%220%22%2C%22bidSubscribe%22:%22-1%22%2C%22vipManager%22:%220%22%2C%22onum%22:%220%22%2C%22monitorUnreadCount%22:%220%22%2C%22discussCommendCount%22:%220%22%2C%22showPost%22:null%2C%22messageBubbleCount%22:%220%22%2C%22claimPoint%22:%220%22%2C%22token%22:%22eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUzODc1MzEwMiIsImlhdCI6MTYwOTc1NjczMCwiZXhwIjoxNjQxMjkyNzMwfQ.SreOzVsgOu055ugHw03sDN04rAtHn_GFZsuR4L-c_LbfRtTmBJiIHok7dYkNoIeQl2XSRw-GK9nKn-ojvxXYlA%22%2C%22schoolAuthStatus%22:%222%22%2C%22userId%22:%2232439427%22%2C%22scoreUnit%22:%22%22%2C%22redPoint%22:%220%22%2C%22myTidings%22:%220%22%2C%22companyAuthStatus%22:%222%22%2C%22originalScore%22:%2245%22%2C%22myAnswerCount%22:%220%22%2C%22myQuestionCount%22:%220%22%2C%22signUp%22:%220%22%2C%22privateMessagePointWeb%22:%220%22%2C%22nickname%22:%22nma%22%2C%22privateMessagePoint%22:%220%22%2C%22bossStatus%22:%222%22%2C%22isClaim%22:%220%22%2C%22yellowDiamondEndTime%22:%220%22%2C%22yellowDiamondStatus%22:%22-1%22%2C%22pleaseAnswerCount%22:%220%22%2C%22bizCardUnread%22:%220%22%2C%22vnum%22:%220%22%2C%22mobile%22:%2218538753102%22%2C%22riskManagement%22:{%22servicePhone%22:null%2C%22mobile%22:18538753102%2C%22title%22:null%2C%22currentStatus%22:null%2C%22lastStatus%22:null%2C%22quickReturn%22:false%2C%22oldVersionMessage%22:null%2C%22riskMessage%22:null}}; tyc-user-info-save-time=1609756732465; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUzODc1MzEwMiIsImlhdCI6MTYwOTc1NjczMCwiZXhwIjoxNjQxMjkyNzMwfQ.SreOzVsgOu055ugHw03sDN04rAtHn_GFZsuR4L-c_LbfRtTmBJiIHok7dYkNoIeQl2XSRw-GK9nKn-ojvxXYlA; tyc-user-phone=%255B%252218538753102%2522%255D; acw_tc=2760823116098373962505096e645d8d715e344814575c09dae5de0120e143; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1609839069
Host: www.tianyancha.com
Referer: https://www.tianyancha.com/search?key=JIANGYIN%20MEIDA%20NEW%20MATERIALS%20CO.%2C%20LTD
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66


    '''

    spider=Spider()
    # spider.Imatate()
    # spider.pb_repair()

    # spider.headers_get(hear)
    spider.headers_eval(hear)

    # print(datetime.now())

