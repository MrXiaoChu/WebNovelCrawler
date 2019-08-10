#!/usr/bin/env python
# coding: utf-8

# In[1]:


#-*- coding: UTF-8 -*-
from bs4 import BeautifulSoup  #記得要解析HTML和XML標記語言，可以用BeautifulSoup，也可以學學PyQuery，這個比較容易使用
from urllib.error import HTTPError #如果遇到404 Not Found，用這個例外處理機制很方便
from collections import OrderedDict #這是有排序的字典型資料結構
import json #符合規範的json標準函式庫
import pprint #可以印出比print函式更容易閱讀的文字
import time #撰寫爬蟲記得要用time函式庫來控制時間
import urllib #Python內建的網頁擷取函式庫，基本上內建的函式庫已經很強大，不一定要用到requests函式庫

#網頁的編碼是GBK(中國區域編碼)
full_dictionary = OrderedDict() #儲存總圖書的字典
library_dictionary = OrderedDict() #儲存一本本小說的字典
author_dictionary =  OrderedDict() #儲存作者的字典
book_dictionary = OrderedDict() #儲存單一一本小說的字典
full_list = list() #資料處理時會用到的暫存字典
chapter_list = list() #儲存章用的字典
key_list = list() #儲存節名稱的字典
loop_page = 5 #控制迴圈的探索次數，是數值的平方

for page in range(0,loop_page): #廣度優先搜尋用迴圈
    for sub_page in range(0,loop_page): #深度優先搜尋用迴圈
        library_dictionary = OrderedDict() #清空一本本小說的數值
        novel_URL = "https://www.wenku8.net/novel/" +  str(page) + "/" + str(sub_page) + "/index.htm" #要爬取的小說網址
        try: #例外處理機制
            response = urllib.request.urlopen(novel_URL) #對網址送出request
            html = response.read() #讀取儲存回傳的網頁資料
            soup = BeautifulSoup(html, "html5lib") #將回傳的網頁資料解析為HTML格式
            print("網址為 {0}".format(novel_URL)) #提示操作人員用的資訊
            print("現在的目錄為 {0} 子目錄為 {1}".format(page, sub_page)) #提示操作人員用的資訊
            print("===" * 10) #分隔表單用的橫線
            table = soup.find_all("td") #分析後確定我們只需要表格<td>內的數據
            print(soup.find(id = "title").get_text()) #抓取小說名稱
            print("    {0}".format(soup.find(id = "info").get_text().replace("作者：", ""))) #抓取作者名稱 
            for td in table: #用迴圈的方式由上而下開始利用字典儲存資料
                for td_child in table: #先把章的字典建立起來的迴圈
                    if "vcss" in str(td_child): #使用字串判斷，含有vcss的HTML是章
                        book_dictionary[str(td_child.get_text())] = chapter_list #建立字典的KEY值
                        chapter_list = list() #但我們不要Value值，所以每一次的迴圈都要清除掉
                key_list = list(book_dictionary.keys()) #暫存KEY值用的串列
                table = list(table) #暫時將BeautifulSoup類別轉為list類別
                book_name_list = list() #清理節的資料
                index = -1 #用於控制儲存章串列的索引
                for book_name in table: #開始抓取節的名稱
                    if "vcss" in str(book_name): #如果遇到章，就觸發清除節串列的資料
                        index += 1 #告訴迴圈要跳到下一個章了。
                        book_name_list = list() #清空節的資料，否則串列會越來越長
                    else: #基本上字串中只要不是沒有vcss的文字，就是小說的節
                        if book_name.get_text() != "\xa0": #在網頁中它空表格會預設儲存為\xa0，這是不要的資料，所以在這裡就清除
                            book_name_list.append(book_name.get_text()) #把小說中的節暫時儲存起來
                            book_dictionary[key_list[index]] = book_name_list #把小說的節儲存到正確的章內
                author_temp = str(soup.find(id = "info").get_text()).replace("作者：", "") #儲存小說的作者，去除「作者：」字串
                library_temp = soup.find(id = "title").get_text() #儲存小說的名稱
                chapter_list = list() #清空節的資料
                break #抓好一本小說後就先跳出迴圈
            author_dictionary[author_temp]  = book_dictionary #把小說名稱作為KEY值
            library_dictionary[library_temp] = author_dictionary #把作者名稱作為KEY值
            author_dictionary = OrderedDict() #儲存作者的字典重新初始化
            book_dictionary = OrderedDict() #小說字典重新初始化
            pprint.pprint(library_dictionary) #印出目前的工作進度
            full_list.append(library_dictionary) #把目前的工作進度站存進list內
            full_dictionary[str(soup.find(id = "title").get_text()) + "的書目詳細資料"] = full_list #建立書庫
            with open(str(soup.find(id = "title").get_text()) + ".json", "w", encoding="utf-8") as fp: #把書庫的資料寫入硬碟
                json.dump(full_dictionary, fp, ensure_ascii = False, indent=4) #以JSON格式儲存
            print("{0}的JSON檔案已輸出".format(str(soup.find(id = "title").get_text()))) #提示檔案儲存的狀態
            full_dictionary = OrderedDict() #儲存總圖書的字典重新初始化
            library_dictionary = OrderedDict() #儲存一本本小說的字典重新初始化
            author_dictionary =  OrderedDict() #儲存作者的字典重新初始化
            book_dictionary = OrderedDict() #小說字典重新初始化
            full_list = list() #資料處理時會用到的暫存字典重新初始化
            chapter_list = list() #儲存節名稱的字典
            key_list = list() #儲存章用的字典重新初始化
            print("暫停1秒鐘") #提示目前程式暫停中
            time.sleep(1) #避免讓小說網站的伺服器附載過大
        except HTTPError: #404 Not Found處理方式
            print("網址 {0} 沒有小說".format(novel_URL)) #提示該網址無效
            print("暫停1秒鐘") #提示目前程式暫停中
            time.sleep(1) #避免讓小說網站的伺服器附載過大
            continue #跳過這階段，繼續執行下一個迴圈
            
            


    


# In[2]:


full_dictionary


# In[ ]:




