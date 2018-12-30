import tkinter as tk
import requests
from bs4 import BeautifulSoup
import os
import time
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model #通过sklearn.linermodel加载岭回归方法
from sklearn import cross_validation #加载交叉验证模块，加载matplotilib模块

headers = {
	       'Accept': '*/*',
               'Accept-Language': 'en-US,en;q=0.8',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
               'Connection': 'keep-alive',
               'Referer': 'http://www.baidu.com/'
}#设置头部信息，模仿浏览器行为，防止反爬虫设置

total = tk.Tk()   
total.title("欢迎来到股票分析器！")
total.resizable(1,1)#宽可变, 高可变

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
    while(index>0):#筛选有用信息，即每日收盘价格、振幅以及换手率
        	resultString += stockData[index].get_text()+'\t'+stockData[index1].get_text()+'\t'+stockData[index2].get_text()+'\n'
        	index=index-11
    return resultString

def createUrl(shareCode,beginYear,endYear):
    shareCodeStr = str(shareCode)

    f = open('./' + shareCodeStr + '.txt', 'a')#写入TXT

    for i in range(beginYear,endYear+1):
        #time.sleep(5)
        for j in range(1,5):
        	temp=sharesCrawl(shareCode,i,j)#按每年每季度爬取
        	#print(temp)
        	f.write(temp)
        	#time.sleep(5)#防止过快访问，被标记为恶意行为
    f.close()

def predict(a,b,c):
	a=str(a)
	data=np.genfromtxt(a+'.txt')
	X=data[:,:2] #X用于保存0-1维数据作为参数
	y=data[:,2] #y用于保存第2维数据作为属性
	poly=PolynomialFeatures(14) #用于创建最高次数14次方的的多项式特征，多次试验后决定采用14次
	X=poly.fit_transform(X) #X为创建的多项式特征
	train_set_X, test_set_X , train_set_y, test_set_y =cross_validation.train_test_split(X,y,test_size=0.3,random_state=0)
	clf=linear_model.Ridge(alpha=1.0,fit_intercept = True)#创建岭回归实例
	clf.fit(train_set_X,train_set_y)#调用fit函数使用训练集训练回归器
	start=100
	end=(int(c)-int(b))*235
	y_pre=clf.predict(X) #是调用predict函数的拟合值
	time=np.arange(start,end)
	plt.plot(time,y[start:end],'b', label="real")
	plt.plot(time,y_pre[start:end],'r', label='predict')#展示真实数据（蓝色）以及拟合的曲线（红色）
	plt.legend(loc='upper left') #设置图例的位置
	plt.show()

def DengLu(Total):
	photo = tk.PhotoImage(file="1.gif",)
	theLabel = tk.Label(Total,   # 将内容绑定在  root 初始框上面
						image=photo,height=200,width=80,   #载入图片
                   		compound=tk.CENTER,bg="#B0C4DE LightSteelBlue 亮钢蓝")   #声明图片的位置

	theLabel.pack(fill=tk.X)     # 自动调整布局
	root = tk.LabelFrame(Total,height=3,width=80, text='请输入股票代码及查询时间范围：',bg="#B0C4DE LightSteelBlue 亮钢蓝")
  
	root.pack(anchor=tk.S,fill=tk.BOTH,padx=0,ipady=10)

	tk.Label(root,text='股票代码 :',bg="#B0C4DE LightSteelBlue 亮钢蓝").grid(row=0,column=0,padx=3,pady=10) # 对Label内容进行 表格式 布局
	tk.Label(root,text='起始日期 :',bg="#B0C4DE LightSteelBlue 亮钢蓝").grid(row=1,column=0,padx=3,pady=10)
	tk.Label(root,text='终止日期 :',bg="#B0C4DE LightSteelBlue 亮钢蓝").grid(row=2,column=0,padx=3,pady=10)
	v1=tk.StringVar()    # 设置变量 . 
	v2=tk.StringVar()
	v3=tk.StringVar()
	e3 = tk.Entry(root,textvariable=v3,bg="#F0F8FF AliceBlue 爱丽丝蓝").grid(row=2,column=1,padx=10,pady=10)      # 进行表格式布局 . 
	e1 = tk.Entry(root,textvariable=v1,bg="#F0F8FF AliceBlue 爱丽丝蓝").grid(row=0,column=1,padx=10,pady=10)      # 用于储存 输入的内容  
	e2 = tk.Entry(root,textvariable=v2,bg="#F0F8FF AliceBlue 爱丽丝蓝").grid(row=1,column=1,padx=10,pady=10)
      # 进行表格式布局 . 

	def show():
		a=v1.get()
		b=v2.get()
		c=v3.get()
		a=int(a)
		b=int(b)
		c=int(c)
		createUrl(a,b,c)
		predict(a,b,c)
		pass
    
	tk.Button(root,text='查询',relief="groove",bg="#87CEFA LightSkyBlue 亮天蓝色",font=("宋体", 15),width=15,command=show).grid(row=3,column=0,sticky=tk.W,padx=10,pady=10)  # 设置 button 指定 宽度 , 并且 关联 函数 , 使用表格式布局 . 
	tk.Button(root,text='退出',relief="groove",bg="#87CEFA LightSkyBlue 亮天蓝色",font=("宋体", 15),width=15,command=Total.quit).grid(row=3,column=1,sticky=tk.E,padx=10,pady=10)
	pass

DengLu(total)
total.mainloop()