# -*- coding: utf-8 -*-

import CrawlMain
import argparse
import sys
import pandas as pd
import time 
import CrawlLatest
from datetime import datetime
import trans
import crawlSearch

#导入库
 
def crawlhistory():
    y = 2020
    v = 88
    # 第一卷为1999y，67v
    while y > 1998 and v > 66:
        for i in range(1,7):
            CrawlMain.CrawlMain(y,v,i)
        y -= 1
        v -= 1
        time.sleep(1)
    pd.DataFrame(CrawlMain.d,columns = CrawlMain.d.keys()).to_csv('../csv/history.csv',index = False)
    return CrawlMain.d

def crawllatest():
    y,v,i = CrawlLatest.getVolumeIssue()
    CrawlMain.CrawlMain(y,v,i)
    pd.DataFrame(CrawlMain.d,columns = CrawlMain.d.keys()).to_csv('../csv/latest.csv',index = False)
    return CrawlMain.d

def crawlspecific(y,i):
    v = int(y) - 1999 + 67
    if i == 'all':
        for j in range(1,7):
            CrawlMain.CrawlMain(y,v,j)
    else:        
        CrawlMain.CrawlMain(y,v,i)
    pd.DataFrame(CrawlMain.d,columns = CrawlMain.d.keys()).to_csv('../csv/specific.csv',index = False)
    return CrawlMain.d

def crawlsearch(text):
    crawlSearch.crawlSearch(text)
    pd.DataFrame(crawlSearch.d,columns = crawlSearch.d.keys()).to_csv('../csv/search.csv',index = False)
    return crawlSearch.d


if __name__ == '__main__':

    arglength = len(sys.argv)
    fhelp = open('../sysinfo/helptxt','r',encoding = 'utf-8')
    helptext = str(fhelp.read())
    warntext = "Invalid Usage: use 'python main.py --help' to get help\n无效参数：请使用'python main.py --help'以获取使用帮助"
    parser = argparse.ArgumentParser()
    parser.add_argument('runtype',type = str,help='选择一种服务类型: \n'+helptext)

    # 因为年份和卷捆绑，所以只要一个参数
    # 如果不输入年份，默认当前年份
    parser.add_argument('-y','--year',type = str, default = datetime.now().year, help = '输入要下载期刊的年份')
    # 如果不输入期，默认所选年份的所有期
    parser.add_argument('-i','--issue',type = str, default = 'all',help = '输入要下载期刊的期数')
    parser.add_argument('-s','--search',type = str, default = 'all',help = '输入要搜索的关键词')


    args=parser.parse_args()
    stype = args.runtype
    y = args.year
    i = args.issue
    s = args.search

    if(stype == 'crawlhistory'):
        crawlhistory()
    elif(stype == 'crawllatest'):
        crawllatest()
    elif(stype == 'crawlspecific'):
        crawlspecific(y,i)
    elif(stype == 'crawlsearch'):
        crawlsearch(s)
    else:
        print(warntext)
