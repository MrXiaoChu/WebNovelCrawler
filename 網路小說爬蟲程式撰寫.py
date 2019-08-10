#!/usr/bin/env python
# coding: utf-8

# In[1]:


#-*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from collections import OrderedDict
import json
import pprint
import time
import urllib

#網頁的編碼是GBK(中國區域編碼)
full_dictionary = OrderedDict()
library_dictionary = OrderedDict()
author_dictionary =  OrderedDict()
book_dictionary = OrderedDict()
full_list = list()
chapter_list = list()
key_list = list()
loop_page = 5

for page in range(0,loop_page):
    for sub_page in range(0,loop_page):
        library_dictionary = OrderedDict()
        novel_URL = "https://www.wenku8.net/novel/" +  str(page) + "/" + str(sub_page) + "/index.htm"
        try:
            response = urllib.request.urlopen(novel_URL)
            html = response.read()
            soup = BeautifulSoup(html, "html5lib")
            print("網址為 {0}".format(novel_URL))
            print("現在的目錄為 {0} 子目錄為 {1}".format(page, sub_page))
            print("===" * 10)
            table = soup.find_all("td")
            print(soup.find(id = "title").get_text())
            print("    {0}".format(soup.find(id = "info").get_text().replace("作者：", "")))
            for td in table:
                for td_child in table:
                    if "vcss" in str(td_child):
                        book_dictionary[str(td_child.get_text())] = chapter_list
                        chapter_list = list()
                key_list = list(book_dictionary.keys())
                table = list(table)
                book_name_list = list()
                index = -1
                for book_name in table:
                    if "vcss" in str(book_name):
                        index += 1
                        book_name_list = list()
                    else:
                        if book_name.get_text() != "\xa0":
                            book_name_list.append(book_name.get_text())
                            book_dictionary[key_list[index]] = book_name_list
                author_temp = str(soup.find(id = "info").get_text()).replace("作者：", "") #去除「作者：」(ok)
                library_temp = soup.find(id = "title").get_text()
                chapter_list = list()
                break
            author_dictionary[author_temp]  = book_dictionary
            library_dictionary[library_temp] = author_dictionary
            author_dictionary = OrderedDict()
            book_dictionary = OrderedDict()
            pprint.pprint(library_dictionary)
            full_list.append(library_dictionary)
            full_dictionary[str(soup.find(id = "title").get_text()) + "的書目詳細資料"] = full_list
            with open(str(soup.find(id = "title").get_text()) + ".json", "w", encoding="utf-8") as fp:
                json.dump(full_dictionary, fp, ensure_ascii = False, indent=4)
            print("{0}的JSON檔案已輸出".format(str(soup.find(id = "title").get_text())))
            full_dictionary = OrderedDict()
            library_dictionary = OrderedDict()
            author_dictionary =  OrderedDict()
            book_dictionary = OrderedDict()
            full_list = list()
            chapter_list = list()
            key_list = list()
            print("暫停1秒鐘")
            time.sleep(1)
        except HTTPError:
            print("網址 {0} 沒有小說".format(novel_URL))
            print("暫停1秒鐘")
            time.sleep(1)
            continue
            
            


    


# In[2]:


full_dictionary


# In[ ]:




