#!/usr/bin/python

import time
import matplotlib.pyplot as plt
import numpy as np
#from scipy.interpolate import spline
from scipy.interpolate import BSpline, make_interp_spline #  Switched to BSpline


filelist = [
            #"t1_output_20240513_bias150_60s.txt",
            "t1_output_20240513_bias150_120s.txt"]
            #"t1_output_20240513_bias250_60s.txt"]

for f in filelist:
#if 1:
    #f = filelist[0]
    content = np.loadtxt(f)
    
    num_list = content[:, 0]
    th_list = content[:, 1]
    ts1_list = content[:, 2]
    ts2_list = content[:, 3]
    pwm_list = content[:, 4] * 24.0/250.0
    timet_list = content[:, 5]
    time_list = timet_list - timet_list[0]
	
    # clip
    '''
    clip_num = 150
    num_list = num_list[:clip_num]
    th_list = th_list[:clip_num]
    ts1_list = ts1_list[:clip_num]
    ts2_list = ts2_list[:clip_num]
    pwm_list = pwm_list[:clip_num]
    timet_list = timet_list[:clip_num]
    time_list = time_list[:clip_num]
    '''

    plt.plot(time_list, th_list)
    
    # 建立繪圖物件 fig, 大小為 12 * 4.5, 內有 1 列 2 欄的小圖, 兩圖共用 x 軸和 y 軸
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex = True, sharey = False, figsize = (12, 9))
    #fig, (ax1, ax2) = plt.subplots(1, 2, sharex = True, sharey = False)

    # 設定小圖 ax1 的坐標軸標籤, 格線顏色、種類、寬度, y軸繪圖範圍, 最後用 plot 繪圖
    ax1.set_xlabel('time (sec)', fontsize = 16)
    ax1.set_ylabel('temp. (C)', fontsize = 16)
    #ax1.grid(color = 'red', linestyle = '--', linewidth = 1)
    ax1.set_ylim(0, 200)
    ax1.plot(time_list, th_list, color = 'blue', linewidth = 1)
    ax1.plot(time_list, ts1_list, color = 'green', linewidth = 1)
    ax1.plot(time_list, ts2_list, color = 'purple', linewidth = 1)
	
    ax1.hlines(95,0,400,color="red")
    ax1.hlines(th_list[0],0,400,color="red")
#    ax1.vlines(250,0,200,color="green")
	

    # 設定小圖 ax2 的坐標軸標籤, 格線顏色、種類、寬度, 最後用 plot 繪圖
    ax2.set_xlabel('time (sec)', fontsize = 16)
    ax2.set_ylabel('vol. (V)', fontsize = 16)
    #ax2.grid(color = 'red', linestyle = '--', linewidth = 1)
    ax2.plot(time_list, pwm_list, color = 'blue', linewidth = 1)


    
    # show some value
    print("==== %s ====" % f)
    # first 95 time
    first_95 = 0
    for ii in range(len(time_list)):
        if ts1_list[ii] >= 95:
            first_95 = ii
            break
    # highest temp
    cur_temp = 0
    high_temp = 0
    for jj in range(1, len(time_list)):
        if ts1_list[jj] > cur_temp:
            high_temp = jj
            cur_temp = ts1_list[jj]

    high_pt = 120
    end_95 = 0
    for kk in range(first_95, len(time_list)):
        if time_list[kk] >= time_list[first_95] + high_pt:
            end_95 = kk
            break

    ax1.vlines(time_list[first_95], 0, 130, color='red')
    ax2.vlines(time_list[first_95], 0, pwm_list[0], color='red')

    ax1.vlines(time_list[end_95], 0, 130, color='red')
    ax2.vlines(time_list[end_95], 0, pwm_list[0], color='red')

    ax1.set_xlim(0, time_list[end_95] + 20)
    ax2.set_xlim(0, time_list[end_95] + 20)


    # initial temp
    print("Init: num = 0, th = %f, ts1 = %f, ts2 = %f" % (th_list[0], ts1_list[0], ts2_list[0]))
    print("To95: num = %d, th = %f, ts1 = %f, ts2 = %f, time = %f" % (first_95, th_list[first_95], ts1_list[first_95], ts2_list[first_95], time_list[first_95]))
    print("End95: num = %d, th = %f, ts1 = %f, ts2 = %f, time = %f" % (end_95, th_list[end_95], ts1_list[end_95], ts2_list[end_95], time_list[end_95]))
    heat_rate = (ts1_list[first_95]-ts1_list[0])/time_list[first_95]
    print("heat rate = %f" % heat_rate)
    print("Highest: num = %d, th = %f, ts1 = %f, ts2 = %f, time = %f" % (high_temp, th_list[high_temp], ts1_list[high_temp], ts2_list[high_temp], time_list[high_temp]))
    # first 95 time + 30s
    # end temp
    ax1.text(time_list[first_95], 175, '(%f, %f)' % (time_list[first_95], ts1_list[first_95]), {'color': 'green'})
    ax1.text(time_list[first_95], 125, '(%f, %f)' % (time_list[first_95], ts2_list[first_95]), {'color': 'purple'})
    ax1.text(time_list[end_95], 175, '(%f, %f)' % (time_list[end_95], ts1_list[end_95]), {'color': 'green'})
    ax1.text(time_list[end_95], 125, '(%f, %f)' % (time_list[end_95], ts2_list[end_95]), {'color': 'purple'})
    

    # 用 savefig 儲存圖片, 用 show 顯示圖片
    fig.suptitle(f[:-3])
    fig.savefig(f[:-3]+'png')
    fig.show()
