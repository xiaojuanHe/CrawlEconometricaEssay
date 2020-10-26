# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import html5lib
import urllib
import pandas as pd
import re
import argparse
import sys
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox 

# GLOBAL VARIABLES
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'
}
d = {'date':[],'doi':[],'href':[],'title':[],'abstract':[]}

# CrawlMain FUNCTION BELOW
def crawlMain(year, volume, issue):
    url = 'https://onlinelibrary.wiley.com/toc/14680262/'
    u = url + str(year) + '/' + str(volume) + '/' + str(issue)
    a = requests.get(u,headers = headers)
    soup = BeautifulSoup(a.content, 'html5lib')

    try:
        soup.find_all(class_ = 'cover-image__date')[0].text
    except Exception:
        print('时间为空')
        return
    else:
        date = soup.find_all(class_ = 'cover-image__date')[0].text

    doi = []
    href = []
    title = []
    abstract = []

    for i in soup.find_all(class_ = 'issue-item__title visitable'):

        try:
            int(i['href'][-1])
        except Exception:
            # print(i['href'],'不是期刊')
            break
        else:            
            title.append(i.text.strip())
            doi.append(i['href'])
            a1 = requests.get('https://onlinelibrary.wiley.com'+i['href'],headers = headers)
            soup1 = BeautifulSoup(a1.content, 'html5lib')
            
            try:
                soup1.find(class_ = 'article-section__content en main').text
            except Exception:
                abstract.append('No abstract！')
            else:
                ab = soup1.find(class_ = 'article-section__content en main').text.strip()
                abstract.append(ab)
            href.append('https://onlinelibrary.wiley.com'+i['href'])

    d['date'].extend([date] * len(doi))
    d['doi'].extend(doi)
    d['href'].extend(href)
    d['abstract'].extend(abstract)
    d['title'].extend(title)

# CrawlLatest FUNCTION BELOW
def getVolumeIssue():
    url = 'https://onlinelibrary.wiley.com/journal/14680262'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'}
    a = requests.get(url,headers = headers)
    soup = BeautifulSoup(a.content, 'html5lib')
    l = re.split(' |,',soup.find(class_ = 'cover-image__parent-item').text)
    y = int(soup.find(class_ = 'cover-image__date').text.split(' ')[-1])
    return y,int(l[1]),int(l[-1])

# CrawlSearch FUNCTION BELOW
def crawlSearch(text): 
    url ='https://onlinelibrary.wiley.com/action/doSearch?AllField=' +  '+'.join(text.strip().split(' ')) + '&SeriesKey=14680262'
    doi = []
    date = []
    href = []
    title = []
    abstract  = []
    a = requests.get(url,headers = headers)
    soup = BeautifulSoup(a.content, 'html5lib')
    for i in soup.find_all(class_ = 'item__body'):
        for j in i.find_all(class_ = 'publication_title visitable'):
            try:
                int(j['href'][-1])
            except Exception:
                # print(j['href'],'不是期刊')
                break
            else:
                doi.append(j['href'])
                href.append('https://onlinelibrary.wiley.com'+j['href'])
                title.append(j.text)
                aburl = 'https://onlinelibrary.wiley.com/action/PB2showAjaxAbstract?doi=' +j['href'].split('/')[2]+'%2F'+j['href'].split('/')[3]+'&isItemAbstract=true'
                a1 = requests.get(aburl,headers = headers)
                soup1 = BeautifulSoup(a1.content, 'html5lib')
                try:
                    soup1.find(class_ = 'article-section__content en main').text
                except Exception:
                    abstract.append('No abstract！')
                else:
                    ab = soup1.find(class_ = 'article-section__content en main').text.strip()
                    abstract.append(aburl)

            date.append(i.find(class_ = 'meta__epubDate').text.strip())
    d['date'].extend(date)
    d['doi'].extend(doi)
    d['href'].extend(href)
    d['abstract'].extend(abstract)
    d['title'].extend(title)

def crawllatest():
    y,v,i = getVolumeIssue()
    crawlMain(y,v,i)
    pd.DataFrame(d,columns = d.keys()).to_csv('latest.csv',index = False)
    tkinter.messagebox.showinfo( "提示","下载好了")
    return d

def latestGUI():
    global wind1
    window.destroy()
    wind1 = tk.Tk()
    wind1.title("Latest")
    screenwidth = wind1.winfo_screenwidth()
    screenheight = wind1.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (500,102, (screenwidth-500)/2, (screenheight-102)/2)
    wind1.geometry(alignstr)
    wind1.resizable(0,0)

    img = tk.PhotoImage(file ='png.gif')
    label_img = tk.Label(wind1,image = img) 
    label_img.pack()
    b1 = tk.Button(wind1, text = '开始',command = crawllatest,width = 8).place(x = 150,y = 70)
    b2 = tk.Button(wind1, text = '返回上一级',command = closeWind1).place(x = 300, y =70)
    # b1.place(x = 120, y = 20)
    # b1.pack(padx = 5,pady = 5)
    wind1.mainloop()

def crawlhistory():
    y = 2020
    v = 88
    # 第一卷为1999y，67v
    while y > 2018 and v > 66:
        for i in range(1,7):
            crawlMain(y,v,i)
        y -= 1
        v -= 1
        time.sleep(1)
    pd.DataFrame(d,columns = d.keys()).to_csv('history.csv',index = False)
    tkinter.messagebox.showinfo( "提示","下载好了")
    return d

def historyGUI():
    global wind2
    window.destroy()
    wind2 = tk.Tk()
    wind2.title("History")
    screenwidth = wind2.winfo_screenwidth()
    screenheight = wind2.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (500,100, (screenwidth-500)/2, (screenheight-100)/2)
    wind2.geometry(alignstr)
    wind2.resizable(0,0)

    img = tk.PhotoImage(file ='png.gif')
    label_img = tk.Label(wind2,image = img) 
    label_img.pack()
    b1 = tk.Button(wind2, text = '开始',command = crawlhistory,width = 8).place(x = 150, y = 70)
    b2 = tk.Button(wind2, text = '返回上一级',command = closeWind2).place(x = 300, y =70)    
    # b1.place(x = 120, y = 20)
    # b1.pack(padx = 5,pady = 5)
    wind2.mainloop()

def crawlspecific(var_year, var_issue):
    try:
        int(var_year.get())
        int(var_issue.get())
    except:
        tkinter.messagebox.showinfo( "提示","请输入合法的数字！")
    y = int(var_year.get())
    i = int(var_issue.get())
    v = int(y) - 1999 + 67
    if i > 6 or i < 1:
        tkinter.messagebox.showinfo( "提示","请输入区间[1,6]内的整数")
    else:
        if i == 'all':
            for j in range(1,7):
                crawlMain(y,v,j)
        else:        
            crawlMain(y,v,i)
        pd.DataFrame(d,columns = d.keys()).to_csv('specific.csv',index = False)
        tkinter.messagebox.showinfo( "提示","下载好了")
    return d

def specificGUI():
    window.destroy()
    global wind3
    wind3 = tk.Tk()
    wind3.title('Specific')
    screenwidth = wind3.winfo_screenwidth()
    screenheight = wind3.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (200,120, (screenwidth-200)/2, (screenheight-120)/2)
    wind3.geometry(alignstr)
    wind3.resizable(0,0)


    tk.Label(wind3, text = '请输入年份：').place(x = 10, y = 20)
    tk.Label(wind3, text = '请输入期数：').place(x = 10,y = 50)

    var_year = tk.StringVar()
    tk.Entry(wind3,textvariable = var_year,width = 10).place(x = 100, y = 20)
    var_issue = tk.StringVar()
    tk.Entry(wind3,textvariable = var_issue,width = 10).place(x = 100, y = 50)

    tk.Button(wind3,text = '开始',command = lambda :crawlspecific(var_year,var_issue),width = 5).place(x=35,y = 86)
    tk.Button(wind3,text = '返回上一级',command = closeWind3).place(x = 110,y=86)
    wind3.mainloop()

def crawlsearch(var_search):
    text = var_search.get()
    crawlSearch(text)
    pd.DataFrame(d,columns = d.keys()).to_csv('search.csv',index = False)
    tkinter.messagebox.showinfo( "提示","下载好了")
    return d

def searchGUI():
    global wind4
    window.destroy()
    wind4 = tk.Tk()
    wind4.title('crawlsearch')

    screenwidth = wind4.winfo_screenwidth()
    screenheight = wind4.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (200,80, (screenwidth-200)/2, (screenheight-80)/2)
    wind4.geometry(alignstr)
    wind4.resizable(0,0)


    tk.Label(wind4, text = '请输入关键字：').place(x = 10, y = 10)

    var_search = tk.StringVar()
    tk.Entry(wind4,textvariable = var_search,width = 12).place(x = 100, y = 10)

    tk.Button(wind4,text = '开始',command = lambda :crawlsearch(var_search)).place(x=35,y = 47)
    tk.Button(wind4,text = '返回上一级',command = closeWind4).place(x = 110, y = 47)
    wind4.mainloop()

def closeWind1():
    wind1.destroy()
    mainGUI()

def closeWind2():
    wind2.destroy()
    mainGUI()

def closeWind3():
    wind3.destroy()
    mainGUI()

def closeWind4():
    wind4.destroy()
    mainGUI()

def mainGUI():
    global window
    window = tk.Tk()
    window.title("爬虫小工具")
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (250,100, (screenwidth-250)/2, (screenheight-100)/2)
    window.geometry(alignstr)
    window.resizable(0,0)

    l1 = tk.Label(window,text = '请选择：')
    l1.grid(column = 1, row = 2, padx = 30, pady = 30)

    var = tk.StringVar()
    ttk1 = ttk.Combobox(window,width = 12, height = 8)
    ttk1.grid(column = 3,row = 2,rowspan = 30)
    ttk1.configure(state = 'readonly')
    ttk1['value'] =['crawlHistory','crawlLatest','crawlSpecific','crawlSearch']
    ttk1.current(0)


    def click(*args):
        if ttk1.get() == 'crawlHistory':
            historyGUI()
        elif ttk1.get() == 'crawlLatest':
            latestGUI()
        elif ttk1.get() == 'crawlSpecific':
            specificGUI()
        else:
            searchGUI()
    b1 = tk.Button(window,text = '开始',command = click,width = 8).place(x = 100 , y =65)

    window.mainloop()

if __name__ == '__main__':
    window = tk.Tk()
    window.title("爬虫小工具")
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (250,100, (screenwidth-250)/2, (screenheight-100)/2)
    window.geometry(alignstr)
    window.resizable(0,0)

    l1 = tk.Label(window,text = '请选择：')
    l1.grid(column = 1, row = 2, padx = 30, pady = 30)

    var = tk.StringVar()
    ttk1 = ttk.Combobox(window,width = 12, height = 8)
    ttk1.grid(column = 3,row = 2,rowspan = 30)
    ttk1.configure(state = 'readonly')
    ttk1['value'] =['crawlHistory','crawlLatest','crawlSpecific','crawlSearch']
    ttk1.current(0)


    def click(*args):
        if ttk1.get() == 'crawlHistory':
            historyGUI()
        elif ttk1.get() == 'crawlLatest':
            latestGUI()
        elif ttk1.get() == 'crawlSpecific':
            specificGUI()
        else:
            searchGUI()
    b1 = tk.Button(window,text = '开始',command = click,width = 8).place(x = 100 , y =65)

    window.mainloop()
