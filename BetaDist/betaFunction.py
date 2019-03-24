import math
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import axes3d
import time

STEP = 10**6  # 积分步数
ZERO = 0.01   # 零值，防止出现0为分母报错的情况


def integrate(target_func, bottom, top, x):
    """积分计算方法
    target_fun: 被积函数
    bottom: 下界
    top: 上界
    x: 参数值"""
    dt = (top-bottom)/STEP
    t_axis = np.linspace(bottom, top, STEP)
    y_axis = dt*target_func(t_axis, x)
    sum = np.sum(y_axis)
    return sum

def gamma_in(t,x):
    """Gamma函数被积函数"""
    return np.power(t, x-1)*np.power(math.e, -t)

def gamma_func(x):
    """Gamma函数"""
    assert x < 101, "the value of 'x' is too large"  # 因为当x取值很大的时候正无穷必须要取很大才会得到比较准确的结果，这里是在个人pc上实验的，为了避免迭代周期过长或者准确度低直接拒绝100以上的值
    if x < 2: # 因为步长的x取值很小的情况下，无穷取得太大没有意义，反而步长过大会显著降低准确度
        INFINITE = 10
    elif x < 100:
        INFINITE = 10e5
    return integrate(gamma_in, ZERO, INFINITE, x)

def beta_func(alpha, beta):
    """beta函数"""
    return gamma_func(alpha)*gamma_func(beta)/gamma_func(alpha+beta)

def beta_dist(p, alpha, beta):
    """beta分布"""
    return np.power(p, (alpha-1))*np.power((1-p), (beta-1))/beta_func(alpha, beta)

def data_gen(p_data, a_data, b):
    """画图数据长生方法"""
    Z = []
    for _x in a_data:
        y_data = beta_dist(p_data, b, _x)
        Z.append(y_data)
    Z = np.transpose(np.array(Z))
    return Z

if __name__ == '__main__':
    p_data = np.linspace(ZERO, 1, 100)

    x_data = np.linspace(ZERO, 10, 100)
    x,p = np.meshgrid(x_data, p_data)

    z_data = []
    for y in np.linspace(0, 10, 100):
        Z = data_gen(p_data, x_data, y)
        z_data.append(Z)


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_zlim(0, 5)

    # Begin plotting.
    wframe = None
    tstart = time.time()
    while 1:
        for z in z_data:
            # If a line collection is already remove it before drawing.
            if wframe:
                ax.collections.remove(wframe)

            # Plot the new wireframe and pause briefly before continuing.
            wframe = ax.plot_wireframe(x, p, z, rstride=2, cstride=2)
            plt.pause(.1)
        print('Average FPS: %f' % (100 / (time.time() - tstart)))
