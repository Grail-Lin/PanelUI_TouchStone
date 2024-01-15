#!/usr/bin/python

import time
import matplotlib.pyplot as plt
import numpy as np
#from scipy.interpolate import spline
from scipy.interpolate import BSpline, make_interp_spline #  Switched to BSpline


filelist = ["20240115_05_75_55_changestatus-2/t1_output.txt", 
            "20240115_05_75_55_changestatus-2/t3_output.txt",
            "20240115_06_75_55_changestatus-3/t1_output.txt", 
            "20240115_06_75_55_changestatus-3/t3_output.txt"]

for f in filelist:
#if 1:
    #f = filelist[0]
    content = np.loadtxt(f)
    
    time_list = content[:, 0]
    tc_list = content[:, 1]
    pwm_list = content[:, 2]
    
	
	
    plt.plot(time_list, tc_list)
    
    # 建立繪圖物件 fig, 大小為 12 * 4.5, 內有 1 列 2 欄的小圖, 兩圖共用 x 軸和 y 軸
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex = True, sharey = False, figsize = (12, 9))
    #fig, (ax1, ax2) = plt.subplots(1, 2, sharex = True, sharey = False)

    # 設定小圖 ax1 的坐標軸標籤, 格線顏色、種類、寬度, y軸繪圖範圍, 最後用 plot 繪圖
    ax1.set_xlabel('time (sec)', fontsize = 16)
    ax1.set_ylabel('temp. (C)', fontsize = 16)
    #ax1.grid(color = 'red', linestyle = '--', linewidth = 1)
    ax1.set_ylim(0, 200)
    ax1.plot(time_list, tc_list, color = 'blue', linewidth = 1)
	
    ax1.hlines(75,0,300,color="red")
    ax1.hlines(55,0,300,color="red")
    ax1.hlines(tc_list[0],0,300,color="red")
    ax1.vlines(250,0,200,color="green")
	

    # 設定小圖 ax2 的坐標軸標籤, 格線顏色、種類、寬度, 最後用 plot 繪圖
    ax2.set_xlabel('time (sec)', fontsize = 16)
    ax2.set_ylabel('vol. (V)', fontsize = 16)
    #ax2.grid(color = 'red', linestyle = '--', linewidth = 1)
    ax2.plot(time_list, pwm_list, color = 'blue', linewidth = 1)

    # 用 savefig 儲存圖片, 用 show 顯示圖片
    fig.savefig(f[:-3]+'png')
    fig.show()
    









