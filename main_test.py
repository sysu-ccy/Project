import numpy as np 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
from numba import jit
from calculator import Methods,Calculator

def creat_plot_3D(x,y,Z,ref1,ref2,save=False):
    X,Y=np.meshgrid(x,y)
    Z1,Z2=Z[:,:,0],Z[:,:,1]
    fig=plt.figure(dpi=100)
    ax1=plt.axes(projection='3d')
    ax1.plot_surface(X,Y,Z1,cmap='rainbow')
    ax1.plot_surface(X,Y,np.ones(Z1.shape)*ref1)
    if save:
        plt.savefig('result1.png')
    else:
        plt.show()

    fig=plt.figure(dpi=100)
    ax2=plt.axes(projection='3d')
    ax2.plot_surface(X,Y,Z2,cmap='rainbow')
    ax2.plot_surface(X,Y,np.ones(Z2.shape)*ref2)
    if save:
        plt.savefig('result2.png')
    else:
        plt.show()

@jit(nopython=True)
def check_values(numbers1,numbers2,ref1,ref2,error1,error2):
    result=[]
    judge=False
    for i in range(numbers1.shape[0]):
        for j in range(numbers1.shape[1]):
            if abs(numbers1[i,j]-ref1)<error1:
                if abs(numbers2[i,j]-ref2)<error2:
                    result.append([i,j])
                    judge=True
    if judge:
        print('True')
        return result
    else:
        print('False')



if __name__ == "__main__":
    cal=Calculator()
    cal.read_excel('Data.xlsx')
    m=cal.M_p[1]
    cal.me.con.set_M_p(m)
    ST_max=cal.ST[1]
    L_s=cal.L_init[1]
    ST_test=np.linspace(0,ST_max,100)
    g_out_test=np.linspace(0,1e-9,100)
    result=np.ones((100,100,2))
    for i in range(100):
        for j in range(100):
            cal.me.cal_ML_simple_B(ST_test[i],L_s,True,g_out_test[j])
            result[i,j,0]=cal.me.L[-1]
            result[i,j,1]=cal.me.g[-1]
    creat_plot_3D(ST_test,g_out_test,result,0.0,cal.me.con.g_in)