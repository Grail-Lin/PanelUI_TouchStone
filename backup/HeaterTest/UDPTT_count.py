#!/usr/bin/python

import time
import numpy as np


filelist = ["t1_output.txt"]

for f in filelist:
#if 1:
    #f = filelist[0]
    content = np.loadtxt(f)
    
    col1_list = content[:, 0]
    col2_list = content[:, 1]
    
    avg_col1 = sum(col1_list[20:120]) / 100.0
    avg_col2 = sum(col2_list[20:120]) / 100.0

    print("file name = %s" % f)
    print("avg col1 = %f" % avg_col1)        	
    print("avg col2 = %f" % avg_col2)        	
	
    









