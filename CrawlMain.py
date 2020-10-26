# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import html5lib
import urllib
import pandas as pd
import trans

 
################################################################################
#####################  GLOBAL VARIABLES  #######################################
################################################################################

url = 'https://onlinelibrary.wiley.com/toc/14680262/'

# 要加header，可以不用cookies，不然被反爬，爬不到什么实质内容
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'
}

# 存储爬到的内容（日期、文章doi，文章下载地址，标题）
d = {'date':[],'doi':[],'href':[],'title':[],'abstract':[],'摘要':[]}

################################################################################
##################### BIG FUNCTION BELOW  ######################################
################################################################################
def CrawlMain(year, volume, issue):
    u = url + str(year) + '/' + str(volume) + '/' + str(issue)
    a = requests.get(u,headers = headers)
    soup = BeautifulSoup(a.content, 'html5lib')
    # print(soup)

    # 防止空网页，导致报错。
    # 例如2020年还有的第6期还没有出就会是空网页
    try:
        soup.find_all(class_ = 'cover-image__date')[0].text
    except Exception:
        print('时间为空')
        return
    else:
        date = soup.find_all(class_ = 'cover-image__date')[0].text
#     date = soup.find_all(class_ = 'cover-image__date')[0].text

    doi = []
    href = []
    title = []
    abstract = []
    chinese = []

    for i in soup.find_all(class_ = 'issue-item__title visitable'):

        #去除非标题的东西
        try:
            int(i['href'][-1])
        except Exception:
            print(i['href'],'不是期刊')
        else:            
            title.append(i.text.strip())
            doi.append(i['href'])
            a1 = requests.get('https://onlinelibrary.wiley.com'+i['href'],headers = headers)
            soup1 = BeautifulSoup(a1.content, 'html5lib')
            
            try:
                soup1.find(class_ = 'article-section__content en main').text
            except Exception:
                abstract.append('No abstract！')
                chinese.append('没有摘要！')
                # print('摘要为空')
            else:
                # print(4)
                ab = soup1.find(class_ = 'article-section__content en main').text.strip()
                # print(5)
                ch = trans.transAb(ab)
                chinese.append(ch)
                abstract.append(ab)
            href.append('https://onlinelibrary.wiley.com'+i['href'])
    # print(5)
    d['date'].extend([date] * len(doi))
    d['doi'].extend(doi)
    d['href'].extend(href)
    d['abstract'].extend(abstract)
    d['title'].extend(title)
    d['摘要'].extend(chinese)
    # print(year,d)
#     return pd.DataFrame(d,columns=['date','title','doi','href','abstract']),d