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
t1 = heater (tec cold)
t2 = sample1
t3 = sample2

pid1 -> t1
pid2 -> t2

Keep monitor: NTC and Thermal Camera

S1: room to target temp. (95)
Use NTC to track t1+t2
if t1 < (130) and t2 < (95)
use pid1 to control heater

if t1 >= 130, enter S2
use pid2 to control heater


if t2 >= 95, enter S3
use pid2 to control heater


S2: half to target temp 95
if t2 >= 95, enter S3
use pid2 to control heater

S3: maintain target temp 95
Use NTC to track temp. till 95.
use pid2 to control heater

if time > target time, enter S4

S4: cooldown to room
do nothing, only read temp


'''


from pyfirmata2 import Arduino, PWM
from PID import PID
import time
import math
#from jataruku import PID                          # Grail, 20231106 PID
#from PIDv2 import PID                             # Grail, 20231106 PID

PORT = 'COM3'
#PORT = Arduino.AUTODETECT

b_USE_TEC = False
targetT1 = 130
targetT2 = 95
ptHighT = 30

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
pid1.setSampleTime(0.1)

# pid2: target = T2, use sample temp to control
pid2 = PID(PID2_Kp, PID2_Ki, PID2_Kd)
pid2.SetPoint = targetT2
pid2.setSampleTime(0.1)

class CoThermal:
    '''
        use relay to control heat with Arduino
    '''
    def __init__(self, current_time=None, t1_ofile=None, t2_ofile=None, 
                 t3_ofile=None):
        
        # output file
        self.t1_ofile = t1_ofile if t1_ofile is not None else None
        self.t2_ofile = t2_ofile if t2_ofile is not None else None
        self.t3_ofile = t3_ofile if t3_ofile is not None else None

        # time
        self.sample_time = 0.1
        self.current_time = current_time if current_time is not None else time.time()
        self.last_time = self.current_time
        

        self.pid1 = pid1
        self.pid2 = pid2

        self.T1 = targetT1
        self.T2 = targetT2
        self.high_pt = ptHighT

        self.state_high_ts = 1
        # s1: climb up, use pid1
        # s2: climb up, use pid2
        # s3: maintain, use pid2
        # s4: cooldown
        
        # temperature sampling rate: 1Hz
        self.samplingRate = 100

        self.temp_heater = 0.0
        self.temp_plate1 = 0.0
        self.temp_plate2 = 0.0

        self.count_heater = 0
        self.count_plate1 = 0
        self.count_plate2 = 0

        self.timestamp_heater = 0
        self.timestamp_plate1 = 0
        self.timestamp_plate2 = 0

        self.last_ts_high = 0
        self.last_ts_low = 0

        self.r1 = 100000
        self.c1 = 4.391855325e-04
        self.c2 = 2.531872891e-04
        self.c3 = -6.257262991e-11

        self._sr = 9900
        self._nr = 98000
        self._bc = 3950
        self._nt = 25.0

        self.board = Arduino(PORT)

        # arduino pwm pin, 3 5 6 9 10 11
        self.pwm_pin_heater1 = 3
        self.board.digital[self.pwm_pin_heater1].mode = PWM
        self.pwm_pin_heater2 = 5
        self.board.digital[self.pwm_pin_heater2].mode = PWM
        
        # relay pin
        #self.relay_pin_bfan = 7
        #self.relay_pin_sfan = 8

        # temperature pin
        # 1 = plate temp., 0 = heater temp.
        self.tp_pin_t1 = 0
        self.tp_pin_t2 = 1
        self.tp_pin_t3 = 2
        
        # reset pins
        self.pinOut(self.pwm_pin_heater1, 0.0)
        self.pinOut(self.pwm_pin_heater2, 0.0)


    def start(self):
        # setting sampling for temperature
        self.board.analog[self.tp_pin_t1].register_callback(self.heaterTP1Callback)
        self.board.analog[self.tp_pin_t2].register_callback(self.sample1TP1Callback)
        self.board.analog[self.tp_pin_t3].register_callback(self.sample2TP1Callback)

        self.board.samplingOn(1000 / self.samplingRate)

        self.board.analog[self.tp_pin_t1].enable_reporting()
        self.board.analog[self.tp_pin_t2].enable_reporting()
        self.board.analog[self.tp_pin_t3].enable_reporting()

    # 
    def heaterTP1Callback(self, data):
        r2, Tc = self.calT(data)
        self.timestamp_heater += (1 / self.samplingRate)
 
        self.count_heater += 1
        self.temp_heater += Tc

        if self.count_heater == 10:
            self.temp_heater /= 10.0
            print("Heater avg TS %f, %f C" % (self.timestamp_heater, self.temp_heater))

            if self.state_high_ts == 1:
                # use heater temp to control PID1

                # check temperature >= high?
                if self.temp_heater >= self.T_high:
                    self.state_high_ts = 2
                    print("temperature > highTP, state_high_ts = 2")
                    self.last_ts_high = self.timestamp_heater
                    # print temp
                    self.controlFlowPrintTPOnly(self.t1_ofile, self.temp_heater, self.timestamp_heater)

                else:
                    pwm = self.controlFlowForPID(self.pid1, self.temp_heater)
                    # print temp
                    self.controlFlowPrintTPOnly(self.t1_ofile, self.temp_heater, self.timestamp_heater, pwm)


            else: # == 2, 3, 4
                self.controlFlowPrintTPOnly(self.t1_ofile, self.temp_heater, self.timestamp_heater)

            # reset temp and count
            self.temp_heater = 0
            self.count_heater = 0

        return


    # plate1TP1 cb, record only
    def sample1TP1Callback(self, data):
        r2, Tc = self.calT(data)
        self.timestamp_plate1 += (1 / self.samplingRate)
 
        self.count_plate1 += 1
        self.temp_plate1 += Tc

        if self.count_plate1 == 10:
            self.temp_plate1 /= 10.0
            print("Plate1 avg TS %f, %f C" % (self.timestamp_plate1, self.temp_plate1))
            #self.controlFlowPrintTPOnly(self.t2_ofile, self.temp_plate1, self.timestamp_plate1)

            if self.state_high_ts == 1:
                # check temperature >= high?
                if self.temp_plate1 >= self.T2:
                    self.state_high_ts = 3
                    print("temperature > highTP, state_high_ts = 3")
                    self.last_ts_high = self.timestamp_heater
                    pwm = self.controlFlowForPID(self.pid2, self.temp_plate1)
                    self.controlFlowPrintTPOnly(self.t2_ofile, self.temp_plate1, self.timestamp_plate1, pwm)
                else:
                    self.controlFlowPrintTPOnly(self.t2_ofile, self.temp_plate1, self.timestamp_plate1, 0.0)
            # do nothing
            elif self.state_high_ts == 2:
                pwm = self.controlFlowForPID(self.pid2, self.temp_plate1)

                if self.temp_plate1 >= self.T2:
                    self.state_high_ts = 3
                    print("temperature > highTP, state_high_ts = 3")
                    self.last_ts_high = self.timestamp_heater

                self.controlFlowPrintTPOnly(self.t2_ofile, self.temp_plate1, self.timestamp_plate1, pwm)

            elif self.state_high_ts == 3:
                if (self.timestamp_plate1 - self.last_ts_high) > self.high_pt:
                    self.state_high_ts = 4
                    print("time period long enough, state_high_ts = 3")
                    self.pinOut(self.pwm_pin_heater, 0.0)
                    self.controlFlowPrintTPOnly(self.t2_ofile, self.temp_plate1, self.timestamp_plate1)

                else:
                    pwm = self.controlFlowForPID(self.pid2, self.temp_plate1)
                    self.controlFlowPrintTPOnly(self.t2_ofile, self.temp_plate1, self.timestamp_plate1, pwm)


            elif self.state_high_ts == 4:

                # cool down
                self.pinOut(self.pwm_pin_heater, 0.0)
                self.controlFlowPrintTPOnly(self.t2_ofile, self.temp_plate1, self.timestamp_plate1)


            # reset temp and count
            self.temp_plate1 = 0
            self.count_plate1 = 0

        return

    # plate2TP1 cb, record only
    def sample2TP1Callback(self, data):
        r2, Tc = self.calT(data)
        #print("TECHeat TS %f,%f:%f Ohm, %f C" % (self.timestamp_plate2, data, r2, Tc))
        self.timestamp_plate2 += (1 / self.samplingRate)
 
        self.count_plate2 += 1
        self.temp_plate2 += Tc

        if self.count_plate2 == 10:
            self.temp_plate2 /= 10.0
            print("Plate2 avg TS %f, %f C" % (self.timestamp_plate2, self.temp_plate2))
            self.controlFlowPrintTPOnly(self.t3_ofile, self.temp_plate2, self.timestamp_plate2)

            self.temp_plate2 = 0
            self.count_plate2 = 0
        return


    def stop(self):
        self.board.samplingOff()
        self.board.exit()
        
    def calTP(self, data):
        r2 = self.r1 * ( 1.0/data - 1.0)
        log_r2 = math.log(r2)
        T = (1.0 / (self.c1 + self.c2 * log_r2 + self.c3 * log_r2 * log_r2 * log_r2))
        Tc = T - 273.15
        return r2, Tc

    def calT(self, data):

        #print("data = %f" % data)
        a1 = self._sr / (1.0/data - 1.0)

        sh = math.log(a1 / self._nr) / self._bc + 1.0 /(self._nt + 273.15)

        Tc = 1.0 / sh - 273.15
        return a1, Tc

    # pin output
    def pinOut(self, pin, value=1.0):
        print("set digital[%d] value: %f" % (pin, value))
        self.board.digital[pin].write(value)

       

    # 20240202
    def controlFlowPrintTPOnly(self, t_ofile, temperature, timestamp, pwm = 0.0):
        '''
            print the data only
        '''
        if t_ofile is not None:
            print("%f\t%f\t%f\t%d" % (timestamp, temperature, pwm, self.state_high_ts), file=t_ofile)

        return

    def controlFlowForPID(self, current_pid, temperature):
        current_pid.update(temperature)

        targetPwm = current_pid.output
        targetPwm = max(min( targetPwm, 100.0 ), 0.0)
        targetPwm = targetPwm / 100.0
        print("targetPwm = %f" % targetPwm)

        self.pinOut(self.pwm_pin_heater1, targetPwm)
        self.pinOut(self.pwm_pin_heater2, targetPwm)
		
        return targetPwm



t1_path = 't1_output.txt'
t2_path = 't2_output.txt'
t3_path = 't3_output.txt'

try: 
    t1_output_f = open(t1_path, 'w')
    t2_output_f = open(t2_path, 'w')
    t3_output_f = open(t3_path, 'w')

    print("Let's print data from Arduino's analog pins for 100secs.")
    # Let's create an instance
    ntc_sensor = CoThermal(t1_ofile=t1_output_f, t2_ofile=t2_output_f, t3_ofile=t3_output_f)
    # and start DAQ
    ntc_sensor.start()
    # let's acquire data for 100secs. We could do something else but we just sleep!
    time.sleep(300)
    # let's stop it
    ntc_sensor.stop()
    print("finished")

except:
    print("Unable to create file on disk.")
    t1_output_f.close()
    t2_output_f.close()
    t3_output_f.close()

finally:
    t1_output_f.close()
    t2_output_f.close()
    t3_output_f.close()


