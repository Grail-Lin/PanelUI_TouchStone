'''
# command format: ntc100k_sensor.py <time_interval=1>
from argparse import ArgumentParser
parser = ArgumentParser()
# add static parameters
parser.add_argument('led_pin', type=int, help='led pin, display an integer in [0,3]')
parser.add_argument('suffix', type=string, help='file suffix, display a string')
args = parser.parse_args()
'''

'''
t1 = tec cold (heater middle)
t2 = sample1 temp
t3 = sample2 temp

create copcb

use
controlPIDBothHeater(self, timeout = 20, pid_p1 = None, pid_p2 = None, p1_target_temp = 130, p2_target_temp = 95, mode = 3)


'''


import copcb
from PID import PID
import time
import math

PORT = 'COM3'
#PORT = Arduino.AUTODETECT

b_USE_TEC = False
targetT1 = 130
targetT2 = 95
ptHighT = 30

'''
# 1
PID1_Kp = 10
PID1_Ki = 1
PID1_Kd = 1

PID2_Kp = 9.1
PID2_Ki = 0.3
PID2_Kd = 1.8

# 2
PID1_Kp = 20
PID1_Ki = 1
PID1_Kd = 1

PID2_Kp = 9.1
PID2_Ki = 0.3
PID2_Kd = 1.8

# 3
PID1_Kp = 30
PID1_Ki = 1
PID1_Kd = 1

PID2_Kp = 9.1
PID2_Ki = 0.3
PID2_Kd = 1.8

# 4
PID1_Kp = 10
PID1_Ki = 1
PID1_Kd = 1

PID2_Kp = 20
PID2_Ki = 0.3
PID2_Kd = 1.8

# 5
PID1_Kp = 10
PID1_Ki = 1
PID1_Kd = 1

PID2_Kp = 30
PID2_Ki = 0.3
PID2_Kd = 1.8

# 6
PID1_Kp = 10
PID1_Ki = 1
PID1_Kd = 1

PID2_Kp = 9.1
PID2_Ki = 1
PID2_Kd = 1.8

# 7
PID1_Kp = 10
PID1_Ki = 1
PID1_Kd = 1

PID2_Kp = 9.1
PID2_Ki = 5
PID2_Kd = 1.8

# 8
PID1_Kp = 10
PID1_Ki = 1
PID1_Kd = 1

PID2_Kp = 9.1
PID2_Ki = 0.3
PID2_Kd = 4

# 9
PID1_Kp = 10
PID1_Ki = 1
PID1_Kd = 1

PID2_Kp = 9.1
PID2_Ki = 0.3
PID2_Kd = 0.9

'''

PID1_Kp = 10
PID1_Ki = 1
PID1_Kd = 1

PID2_Kp = 9.1
PID2_Ki = 0.3
PID2_Kd = 1.8

'''
P = 10
I = 1
D = 1


HET_Kp = 9.1;         # 12 數值是否能達到目標值
HET_Ki = 0.3;         # 0.05 誤差積累
HET_Kd = 1.8;#1.8;         # 35 誤差變化率
TEC_Kp = 200;         # 200 數值是否能達到目標值
TEC_Ki = 10;          # 10 誤差積累
TEC_Kd = 5;           # 5 誤差變化率
'''

# pid1: target = T1, use heater mid temp to control
pid1 = PID(PID1_Kp, PID1_Ki, PID1_Kd)
pid1.SetPoint = targetT1
pid1.setSampleTime(1)

# pid2: target = T2, use sample temp to control
pid2 = PID(PID2_Kp, PID2_Ki, PID2_Kd)
pid2.SetPoint = targetT2
pid2.setSampleTime(1)


class CoThermal:
    '''
        use relay to control heat with Arduino
    '''
    def __init__(self, current_time=None, amp = 5.0, t1_ofile=None): #, t2_ofile=None, t3_ofile=None):

        self.amp = amp
        self.btpcb = copcb.ModuleBT()
        self.btpcb.initPCB()

        # output file
        self.t1_ofile = t1_ofile if t1_ofile is not None else None
        #self.t2_ofile = t2_ofile if t2_ofile is not None else None
        #self.t3_ofile = t3_ofile if t3_ofile is not None else None

        # time
        self.sample_time = 1
        self.current_time = current_time if current_time is not None else time.time()
        self.last_time = self.current_time
        
        self.pid1 = pid1
        self.pid2 = pid2

        self.T1 = targetT1
        self.T2 = targetT2
        self.high_pt = ptHighT

        self.state_high_ts = 1

        self.timestamp_plate = 0
        self.timestamp_teccool = 0
        self.timestamp_techeat = 0

        self.last_ts_high = 0
        self.last_ts_low = 0
        self.last_ts_env = 0
        self.cur_cycle_time = 0
        self.goal = 0

    def start(self, times = 900):
        

        for num in range(times):

            if self.state_high_ts == 1:
                print("state_high_ts = %d" % self.state_high_ts)
                # use controlPIDBothHeater_spec to control Heater
                temp_h, temp_s1, temp_s2, pwm = self.btpcb.controlPIDBothHeater_spec(20, self.pid1, self.pid2, targetT1, targetT2, 3, self.amp)
                #def controlPIDBothHeater_spec(self, timeout = 20, pid_p1 = None, pid_p2 = None, p1_target_temp = 130, p2_target_temp = 95, mode = 3):
                # return t1, t2, t3, pwm
                # need to return value for output
                if self.t1_ofile is not None:
                    print("%d\t%f\t%f\t%f\t%f\t%f" % (num, temp_h, temp_s1, temp_s2, pwm, time.time()), file=self.t1_ofile)
                # if the sample temp >= self.T2, self.state_high_ts = 2, goal = num + self.high_pt * 10
                if temp_s1 >= self.T2:
                    self.state_high_ts = 2
                    self.goal = time.time() + self.high_pt
            elif self.state_high_ts == 2:
                print("state_high_ts = %d" % self.state_high_ts)
                # use controlPIDBothHeater_spec to control Heater
                temp_h, temp_s1, temp_s2, pwm = self.btpcb.controlPIDBothHeater_spec(20, self.pid1, self.pid2, targetT1, targetT2, 3, self.amp)
                # need to return value for output
                if self.t1_ofile is not None:
                    print("%d\t%f\t%f\t%f\t%f\t%f" % (num, temp_h, temp_s1, temp_s2, pwm, time.time()), file=self.t1_ofile)
                # if num == goal, self.state_high_ts = 3
                if time.time() >= self.goal:
                    self.state_high_ts = 3
                    self.btpcb.controlBothHeater(20, 0, 0)
            else:
                print("state_high_ts = %d" % self.state_high_ts)
                # record temp only
                temp_h, temp_s1, temp_s2 = self.btpcb.readTemp_spec(20)
                if self.t1_ofile is not None:
                    print("%d\t%f\t%f\t%f\t0\t%f" % (num, temp_h, temp_s1, temp_s2, time.time()), file=self.t1_ofile)


            # sleep for 0.1 sec
            time.sleep(0.2)

        return


    def start2(self, times = 90):
        sleeptime = 0.05 # 0.05
        for num in range(times):
            # query 12v voltage
            v1 = self.btpcb.get12voltageSystem()
            # sleep for 0.3/6 = 0.05 ( or 0.5/6 = 0.083)
            time.sleep(sleeptime)
            # query 24v voltage
            v2 = self.btpcb.get24voltageSystem()
            # sleep for 0.3/6 = 0.05 ( or 0.5/6 = 0.083)
            time.sleep(sleeptime)
            # query system temp
            tt = self.btpcb.measureSystem()

            if self.t1_ofile is not None:
                print("%d\t%f\t%f\t%f\t%f" % (num, v1, v2, tt, time.time()), file=self.t1_ofile)

            time.sleep(sleeptime)
        return

t1_path = 't1_output_20240516_bias200_30s.txt'
ampify = 200.0

try: 
    t1_output_f = open(t1_path, 'w')
    print("Let's print data from Arduino's analog pins for 100secs.")
    # Let's create an instance
    ntc_sensor = CoThermal(amp = ampify, t1_ofile=t1_output_f)#, t2_ofile=t2_output_f, t3_ofile=t3_output_f)
    # and start DAQ
    #ntc_sensor.start2(500)
    ntc_sensor.start(600)    # 0.2 sec * 900 = 180 sec = 3 min
    # let's acquire data for 100secs. We could do something else but we just sleep!
    print("finished")

except:
    print("Unable to create file on disk.")
    print(sys.exc_info()[0])
    t1_output_f.close()

finally:
    t1_output_f.close()


