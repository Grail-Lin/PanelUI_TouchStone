#!/usr/bin/python

import time
import matplotlib.pyplot as plt
import numpy as np
#from scipy.interpolate import spline
from scipy.interpolate import BSpline, make_interp_spline #  Switched to BSpline


'''
    read file1: PID control
	     file2: Other
		 file3: Other

    



'''
f1 = "20240126_05_95_55_changestatus-5_PID_Plate1023/t1_output.txt"
f2 = "20240126_05_95_55_changestatus-5_PID_Plate1023/t2_output.txt"
f3 = "20240126_05_95_55_changestatus-5_PID_Plate1023/t3_output.txt"

value_f1 = "Plate1(PID)"
value_f2 = "Heater"
value_f3 = "Plate2"


'''
filelist = ["20240126_04_95_55_changestatus-5_PID_Plate2103/t1_output.txt", 
            "20240126_04_95_55_changestatus-5_PID_Plate2103/t2_output.txt",
            "20240126_04_95_55_changestatus-5_PID_Plate2103/t3_output.txt",
            "20240126_05_95_55_changestatus-5_PID_Plate1023/t1_output.txt", 
            "20240126_05_95_55_changestatus-5_PID_Plate1023/t2_output.txt",
            "20240126_05_95_55_changestatus-5_PID_Plate1023/t3_output.txt",
            "20240126_06_95_55_changestatus-5_PID_Heater0123/t1_output.txt", 
            "20240126_06_95_55_changestatus-5_PID_Heater0123/t2_output.txt",
            "20240126_06_95_55_changestatus-5_PID_Heater0123/t3_output.txt"]

for f in filelist:
'''

def calValue(high, low, tc_list, time_list, pwm_list):
    '''
        find first point > low after T0
        find first point > high after T0

        find first point < high after Tx
        find first point < low  after Tx

    '''
    for ii in range(len(pwm_list) - 2):
        if pwm_list[ii] == 0 and pwm_list[ii+1] == 0 and pwm_list[ii+2] == 0:
            t0 = ii
            break

    for ii in range(len(tc_list)):
        if tc_list[ii] > low:
            t1 = ii
            break

    for ii in range(len(tc_list)):
        if tc_list[ii] > high:
            t2 = ii
            break

    for ii in range(len(tc_list[t0:])):
        if tc_list[t0+ii] < high:
            t3 = t0+ii
            break

    for ii in range(len(tc_list[t3:])):
        if tc_list[t3+ii] < low:
            t4 = t3+ii
            break

    heatup_speed = (tc_list[t2] - tc_list[t1])/(time_list[t2] - time_list[t1])
    cooldown_speed = (tc_list[t3] - tc_list[t4])/(time_list[t4] - time_list[t3])

    print("t1 = %d, t2 = %d, t3 = %d, t4 = %d" % (t1, t2, t3, t4))
    print("heatup: %f, cooldown: %f" % (heatup_speed, cooldown_speed))

    return (heatup_speed, cooldown_speed)


if 1:
    #f = filelist[0]
    highT = 95
    lowT = 55

    content1 = np.loadtxt(f1)
    content2 = np.loadtxt(f2)
    content3 = np.loadtxt(f3)
    
    #time_list = content[:, 0]
    time_list = np.arange(0, 900.2, 0.1)
    tc1_list = content1[:, 1]
    pwm_list = content1[:, 2]
    
    tc2_list = content2[:, 1]
    tc3_list = content3[:, 1]
	
	
    #plt.plot(time_list, tc_list)
    
    # 建立繪圖物件 fig, 大小為 12 * 4.5, 內有 1 列 2 欄的小圖, 兩圖共用 x 軸和 y 軸
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex = True, sharey = False, figsize = (12, 9))

    # 設定小圖 ax1 的坐標軸標籤, 格線顏色、種類、寬度, y軸繪圖範圍, 最後用 plot 繪圖
    ax1.set_xlabel('time (sec)', fontsize = 16)
    ax1.set_ylabel('temp. (C)', fontsize = 16)
    #ax1.grid(color = 'red', linestyle = '--', linewidth = 1)
    ax1.set_ylim(0, 200)
    ax1.plot(time_list, tc1_list, color = 'blue', linewidth = 1)
    ax1.plot(time_list, tc2_list, color = 'orange', linewidth = 1)
    ax1.plot(time_list, tc3_list, color = 'green', linewidth = 1)
	
    ax1.legend([value_f1, value_f2, value_f3])




    ax1.hlines(highT,0,time_list[-1],color="red")
    ax1.hlines(lowT,0,time_list[-1],color="red")
    #ax1.hlines(tc_list[0],0,time_list[-1],color="red")
    ax1.vlines(250,0,200,color="green")
	

    # 設定小圖 ax2 的坐標軸標籤, 格線顏色、種類、寬度, 最後用 plot 繪圖
    ax2.set_xlabel('time (sec)', fontsize = 16)
    ax2.set_ylabel('vol. (V)', fontsize = 16)
    #ax2.grid(color = 'red', linestyle = '--', linewidth = 1)
    ax2.plot(time_list, pwm_list, color = 'blue', linewidth = 1)

    # 用 savefig 儲存圖片, 用 show 顯示圖片
    fig.savefig(f1[:-3]+'png')
    fig.show()
    
    print(value_f1)
    calValue(highT - 10, lowT + 5, tc1_list, time_list, pwm_list)
    print(value_f2)
    calValue(highT - 10, lowT + 5, tc2_list, time_list, pwm_list)
    print(value_f3)
    calValue(highT - 10, lowT + 5, tc3_list, time_list, pwm_list)








