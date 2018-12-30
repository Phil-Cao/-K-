import requests
from bs4 import BeautifulSoup
import os
import time

headers = {
	       'Accept': '*/*',
               'Accept-Language': 'en-US,en;q=0.8',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
               'Connection': 'keep-alive',
               'Referer': 'http://www.baidu.com/'
}#设置头部信息，模仿浏览器行为，防止反爬虫设置

def sharesCrawl(shareCode,year,season):
    shareCodeStr = str(shareCode)
    yearStr = str(year)
    seasonStr = str(season)
    url = 'http://quotes.money.163.com/trade/lsjysj_' + shareCodeStr + '.html?year=' + yearStr + '&season=' + seasonStr#设置防虫地址
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'lxml')
    stockData = soup.select('div.inner_box > table > tr > td')#获取网页中的有效信息
    #print(len(stockData))
    index=len(stockData)-1
    index1=len(stockData)-2
    index2=len(stockData)-7
    resultString = ''
    while(index>0):#筛选有用信息，即每日收盘价格
        	resultString += stockData[index].get_text()+'\t'+stockData[index1].get_text()+'\t'+stockData[index2].get_text()+'\n'
        	index=index-11
    return resultString

def createUrl(shareCode,beginYear,endYear):
    shareCodeStr = str(shareCode)

    f = open('./' + shareCodeStr + '.txt', 'a')#写入TXT

    for i in range(beginYear,endYear+1):
        time.sleep(5)
        for j in range(1,5):
        	temp=sharesCrawl(shareCode,i,j)#按每年每季度爬取
        	#print(temp)
        	f.write(temp)
        	time.sleep(5)#防止过快访问，被标记为恶意行为
    f.close()

if __name__=="__main__":
	a=input("please input your stock's code: ")
	b=input("please input the begintime: ")
	c=input("please input the end time: ")
	a=int(a)
	b=int(b)
	c=int(c)
	createUrl(a,b,c)
    #createUrl(601857,2010,2011)
