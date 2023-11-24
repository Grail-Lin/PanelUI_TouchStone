'''
# command format: ntc100k_sensor.py <time_interval=1>
from argparse import ArgumentParser
parser = ArgumentParser()
# add static parameters
parser.add_argument('led_pin', type=int, help='led pin, display an integer in [0,3]')
parser.add_argument('suffix', type=string, help='file suffix, display a string')
args = parser.parse_args()
'''

from pyfirmata2 import Arduino
import PID
import time
import math

#PORT = 'COM5'
PORT = Arduino.AUTODETECT


targetT = 90
P = 10
I = 1
D = 1

pid = PID.PID(P, I, D)
pid.SetPoint = targetT
pid.setSampleTime(1)



class CoThermal:
    '''
        compine PID and Arduino
    '''
    def __init__(self, pid, output_file_1 = None, output_file_2 = None):
        # heater_pin
        self.pid = pid
        self.T_low = 50
        self.T_high = 90
        self.heater_pin = 7
        self.inc_pt = 20
        self.dec_pt = 20
        self.high_pt = 10
        self.low_pt = 10
        self.total_pt = 60

        # sampling rate: 1Hz
        self.samplingRate = 1
        self.timestamp = 0
        self.timestamp2 = 0
        self.r1 = 100000
        self.c1 = 4.391855325e-04
        self.c2 = 2.531872891e-04
        self.c3 = -6.257262991e-11
        '''
        self.r1 = 100000
        self.c1 = 6.66082410500e-04
        self.c2 = 2.23928204100e-04
        self.c3 = 7.19951882000e-08
        '''
        '''
        self.r1 = 10000
        self.c1 = 1.009249522e-03
        self.c2 = 2.378405444e-04
        self.c3 = 2.019202697e-07
        '''
        self.board = Arduino(PORT)
        
        # output file
        self.output_file_1 = output_file_1 if output_file_1 is not None else None
        self.output_file_2 = output_file_2 if output_file_2 is not None else None

    def start(self):
        self.board.analog[0].register_callback(self.myPrintCallback)
        #self.board.analog[2].register_callback(self.myPrintCallback2)

        self.board.samplingOn(1000 / self.samplingRate)

        self.board.analog[0].enable_reporting()
        #self.board.analog[2].enable_reporting()



        
    def myPrintCallback(self, data):
        r2, Tc = self.calT(data)
        print("a0: %f,%f:%f Ohm, %f C" % (self.timestamp, data, r2, Tc))
        self.timestamp += (1 / self.samplingRate)

        if self.output_file_1 is not None:
            print("%f\t%f\t%f" % (self.timestamp, Tc, 0), file=self.output_file_1)

        #self.controlFlow(Tc, self.timestamp)
        
        '''
        if Tc < self.T_high:
            self.turnOnOff(1)
            print("turn heater on")
        else: 
            self.turnOnOff(0)
            print("turn heater off")
        '''

    def myPrintCallback2(self, data):
        r2, Tc = self.calT(data)
        print("a2: %f,%f:%f Ohm, %f C" % (self.timestamp2, data, r2, Tc))
        self.timestamp2 += (1 / self.samplingRate)
        if self.output_file_2 is not None:
            print("%f\t%f\t%f" % (self.timestamp2, Tc, 0), file=self.output_file_2)
    
    def stop(self):
        self.board.samplingOff()
        self.board.exit()
        
    def calT(self, data):
        r2 = self.r1 * ( 1.0/data - 1.0)
        log_r2 = math.log(r2)
        T = (1.0 / (self.c1 + self.c2 * log_r2 + self.c3 * log_r2 * log_r2 * log_r2))
        Tc = T - 273.15
        return r2, Tc

    def turnOnOff(self, value=1):
        self.board.digital[self.heater_pin].write(value)

    def controlFlow(self, temperature, timestamp):
        '''
            T_low to T_high --> inc_period_time
            stay in T_high --> high_period_time
            T_high to T_low --> dec_period_time
            stay in T_low --> low_period_time
        '''
        
        if timestamp < inc_pt:
            '''
                T_low to T_high
            '''
            if temperature > self.T_high:
                self.turnOnOff(0)
            else:
                self.turnOnOff(1)
        elif timestamp < inc_pt + high_pt:
            '''
                stay in T_high
            '''
            if temperature < self.T_high:
                self.turnOnOff(0)
            else:
                self.turnOnOff(1)
        elif timestamp < inc_pt + high_pt + dec_pt:
            '''
                T_high to T_low
            '''
            if temperature < self.T_low:
                self.turnOnOff(1)
            else:
                self.turnOnOff(0)
        else:
            '''
                stay in T_low
            '''
            if temperature < self.T_low:
                self.turnOnOff(1)
            else:
                self.turnOnOff(0)


output_path_1 = 'output_temp3.txt'
output_path_2 = 'output_temp4.txt'


try:
    output_1_f = open(output_path_1, 'w')
    output_2_f = open(output_path_2, 'w')

    print("Let's print data from Arduino's analog pins for 30secs.")
    # Let's create an instance
    ntc_sensor = CoThermal(pid, output_file_1 = output_1_f, output_file_2 = output_2_f)
    # and start DAQ
    ntc_sensor.start()
    # let's acquire data for 10secs. We could do something else but we just sleep!
    time.sleep(300)
    # let's stop it
    ntc_sensor.stop()
    print("finished")

except:
    print("Unable to create file on disk.")
    output_1_f.close()
    output_2_f.close()

finally:
    output_1_f.close()
    output_2_f.close()


'''
print("press Ctrl-C to terminate this program")

try:
    while True:
        # read input analog_0
        # calculate temperature

        # print temperature
        print value
        # time interval
        time.sleep(TIME_INTERVAL)
        
except KeyboardInterrupt:
    pass
'''