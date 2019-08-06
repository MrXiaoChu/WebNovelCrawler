#!/usr/bin/env python
# coding: utf-8

# In[1]:


#-*- coding: UTF-8 -*-
import urllib
import pprint
import time
import json
from urllib.error import HTTPError
from bs4 import BeautifulSoup


# In[2]:


#網頁的編碼是GBK(中國區域編碼)
library_dictionary = dict()
book_dictionary = dict()
chapter_list = list()

for page in range(0,50):
    for sub_page in range(0,50):
        novel_URL = "https://www.wenku8.net/novel/" +  str(page) + "/" + str(sub_page) + "/index.htm"
        try:
            response = urllib.request.urlopen(novel_URL)
            html = response.read()
            soup = BeautifulSoup(html, "html5lib")
            print("網址為 {0}".format(novel_URL))
            print("現在的目錄為 {0} 子目錄為 {1}".format(page, sub_page))
            print("===" * 10)
            
            
            
            table = soup.find_all("td")
            for tr in table:
                
                print(soup.find(id = "title").get_text())
                print("    {0}".format(soup.find(id = "info").get_text().replace("作者：", "")))
                library_dictionary["書本名稱"]  = str(soup.find(id = "title").get_text())
                author_temp = str(soup.find(id = "info").get_text()).replace("作者：", "")
                library_dictionary["作者名稱"]  = str(soup.find(id = "info").get_text())
                for td in table:
                    print("        {0}".format(td.get_text()))
                    
                    if "vcss" in str(td):
                        temp = str(td.get_text())
                        book_dictionary["卷數"] = temp
                        book_dictionary[temp] = chapter_list
                        
                    
                    if "ccss" in str(td):
                        chapter_list.append(str(td.get_text()))
                        
                    #chapter_list = list()
                    library_dictionary["書庫"] = book_dictionary
                break
            book_dictionary = dict()
            break
            print("暫停1秒鐘")
            time.sleep(1)
        except HTTPError:
            print("網址 {0} 沒有小說".format(novel_URL))
            print("暫停1秒鐘")
            time.sleep(1)
            continue


# In[3]:


library_dictionary


# In[4]:


with open('01.json', 'w', encoding='utf-8') as fp:
    json.dump(library_dictionary, fp, ensure_ascii = False, indent=4)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




