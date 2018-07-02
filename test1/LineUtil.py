import numpy as np
from scipy.optimize import leastsq



###需要拟合的函数func及误差error###
def func(p,x):
    k,b=p
    return k*x+b

def error(p,x,y,s):
    # print s
    return func(p,x)-y #x、y都是列表，故返回值也是个列表
        # return func(p, x) - y  # x、y都是列表，故返回值也是个列表

def getLineK(ma20Array):
    s = "Test the number of iteration"
    Xi = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
    Yi = np.array(ma20Array);
    #Yi = np.array([100,110,110,110,110,110,110,110,110,115]);
    p0 = [100, 2]
    Para = leastsq(error, p0, args=(Xi, Yi,s))  # 把error函数中除了p以外的参数打包到args中
    k, b = Para[0]
    x = np.linspace(0, 20, 20)
    # print(x)
    y = k * x + b
    print(y)
    return (y[19]-y[0])/(Xi[19]-Xi[0]);
