# -*- coding: utf-8 -*-

import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib
import trans

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'
}

d = {'date':[],'doi':[],'href':[],'title':[],'abstract':[],'摘要':[]}
def crawlSearch(text):
    url ='https://onlinelibrary.wiley.com/action/doSearch?AllField=' +  '+'.join(text.strip().split(' ')) + '&SeriesKey=14680262'
    doi = []
    date = []
    href = []
    title = []
    abstract  = []
    chineseab = []
    a = requests.get(url,headers = headers)
    soup = BeautifulSoup(a.content, 'html5lib')
    for i in soup.find_all(class_ = 'item__body'):
        for j in i.find_all(class_ = 'publication_title visitable'):
            try:
                int(j['href'][-1])
            except Exception:
                print(j['href'],'不是期刊')
                break
            else:
                doi.append(j['href'])
                href.append('https://onlinelibrary.wiley.com'+j['href'])
                title.append(j.text)
                aburl = 'https://onlinelibrary.wiley.com/action/PB2showAjaxAbstract?doi=' +j['href'].split('/')[2]+'%2F'+j['href'].split('/')[3]+'&isItemAbstract=true'
                a1 = requests.get(aburl,headers = headers)
                soup1 = BeautifulSoup(a1.content, 'html5lib')
                ab = soup1.find_all(class_ = 'article-section__content en main')[0].text.strip()
                ch = trans.transAb(ab)
                abstract.append(ab)
                chineseab.append(ch)
            date.append(i.find(class_ = 'meta__epubDate').text.strip())
    d['date'].extend(date)
    d['doi'].extend(doi)
    d['href'].extend(href)
    d['abstract'].extend(abstract)
    d['title'].extend(title)
    d['摘要'].extend(chineseab)