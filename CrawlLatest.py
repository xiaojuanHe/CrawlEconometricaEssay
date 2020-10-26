# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
import html5lib
import urllib


url = 'https://onlinelibrary.wiley.com/journal/14680262'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'
}

def getVolumeIssue():
    a = requests.get(url,headers = headers)
    soup = BeautifulSoup(a.content, 'html5lib')

    l = re.split(' |,',soup.find(class_ = 'cover-image__parent-item').text)
    y = int(soup.find(class_ = 'cover-image__date').text.split(' ')[-1])
    return y,int(l[1]),int(l[-1])