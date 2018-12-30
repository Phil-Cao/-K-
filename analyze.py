import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model #通过sklearn.linermodel加载岭回归方法
from sklearn import cross_validation #加载交叉验证模块，加载matplotilib模块

#a = input("please input your stock's code: ")
data=np.genfromtxt('601857.txt')
X=data[:,:2] #X用于保存0-1维数据
y=data[:,2] #y用于保存第2维数据
poly=PolynomialFeatures(14) #用于创建最高次数6次方的的多项式特征，多次试验后决定采用6次
X=poly.fit_transform(X) #X为创建的多项式特征
train_set_X, test_set_X , train_set_y, test_set_y =cross_validation.train_test_split(X,y,test_size=0.3,random_state=0)
clf=linear_model.Ridge(alpha=1.0,fit_intercept = True)
#接下来我们创建岭回归实例
clf.fit(train_set_X,train_set_y)
#调用fit函数使用训练集训练回归器
clf.score(test_set_X,test_set_y)
#利用测试集计算回归曲线的拟合优度，clf.score返回值为0.7375
start=250 #接下来我们画一段250到1900范围内的拟合曲线
end=1900
y_pre=clf.predict(X) #是调用predict函数的拟合值
time=np.arange(start,end)
plt.plot(time,y[start:end],'b', label="real")
plt.plot(time,y_pre[start:end],'r', label='predict')
#展示真实数据（蓝色）以及拟合的曲线（红色）
plt.legend(loc='upper left') #设置图例的位置
plt.show()
