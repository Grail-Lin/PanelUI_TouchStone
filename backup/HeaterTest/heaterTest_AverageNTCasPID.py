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
t1 = plate(heater)
t2 = tec cold
t3 = tec hot
t4 = tube temperature, detect by thermal camera

Keep monitor: NTC and Thermal Camera

S1: room to 55
Use NTC to track temp. till 55.
PID with heater

S2: maintain 55
PID with heater, keep 55

S3: 55 to 95
Use NTC to track temp. till 95.
PID with heater

S4: maintain 95
Use NTC to track temp. till 95.
PID with heater

S5: 95 to 55
Stop heater, turn on Fan, till 55

Loop to S2

S6: any to room
'''



from pyfirmata2 import Arduino, PWM
#from jataruku import PID                          // Grail, 20231106 PID
from PID import PID
#from PIDv2 import PID                                       # Grail, 20231106 PID
import time
import math

PORT = 'COM3'
#PORT = Arduino.AUTODETECT

b_USE_TEC = False
targetHighT = 95
targetLowT = 55

'''
P = 10
I = 1
D = 1
'''
HET_Kp = 9.1;         # 12 數值是否能達到目標值
HET_Ki = 0.3;         # 0.05 誤差積累
HET_Kd = 1.8;#1.8;         # 35 誤差變化率
TEC_Kp = 200;         # 200 數值是否能達到目標值
TEC_Ki = 10;          # 10 誤差積累
TEC_Kd = 5;           # 5 誤差變化率

'''
# heater to 95
pid_high = PID.PID(P, I, D)
pid_high.SetPoint = targetHighT
pid_high.setSampleTime(1)

# tec to 55
pid_low = PID.PID(P, I, D)
pid_low.SetPoint = targetLowT
pid_low.setSampleTime(1)

pid_tec = PID.PID(P, I, D)
pid_tec.SetPoint = targetLowT
pid_tec.setSampleTime(1)
'''
# heater to 95
pid_high = PID(HET_Kp, HET_Ki, HET_Kd)
pid_high.SetPoint = targetHighT
pid_high.setSampleTime(0.1)

# tec to 55
pid_low = PID(HET_Kp, HET_Ki, HET_Kd)
pid_low.SetPoint = targetLowT
pid_low.setSampleTime(0.1)

pid_tec = PID(TEC_Kp, TEC_Ki, TEC_Kd)
pid_tec.SetPoint = targetLowT
pid_tec.setSampleTime(0.1)



class CoThermal:
    '''
        use relay to control heat with Arduino
    '''
    def __init__(self, current_time=None, t1_ofile=None, t2_ofile=None, 
                 t3_ofile=None, t4_ofile=None):
        
        # output file
        self.t1_ofile = t1_ofile if t1_ofile is not None else None
        self.t2_ofile = t2_ofile if t2_ofile is not None else None
        self.t3_ofile = t3_ofile if t3_ofile is not None else None
        self.t4_ofile = t4_ofile if t4_ofile is not None else None

        # time
        self.sample_time = 0.1
        self.current_time = current_time if current_time is not None else time.time()
        self.last_time = self.current_time
        

        self.pid_high = pid_high
        self.pid_low = pid_low
        self.pid_tec = pid_tec

        self.T_low = targetLowT
        self.T_high = targetHighT
        self.high_pt = 30
        self.low_pt = 30

        self.state_high_ts = 1
        
        # temperature sampling rate: 1Hz
        self.samplingRate = 100

        self.temp_plate = 0.0
        self.temp_teccool = 0.0
        self.temp_techeat = 0.0

        self.count_plate = 0
        self.count_teccool = 0
        self.count_techeat = 0


        self.timestamp_plate = 0
        self.timestamp_teccool = 0
        self.timestamp_techeat = 0

        self.last_ts_high = 0
        self.last_ts_low = 0
        self.last_ts_env = 0
        self.cur_cycle_time = 0

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
        self._sr = 9900
        self._nr = 98000
        self._bc = 3950
        self._nt = 25.0


        self.board = Arduino(PORT)

        # arduino pwm pin, 3 5 6 9 10 11
        self.pwm_pin_heater = 3
        self.board.digital[self.pwm_pin_heater].mode = PWM
        self.pwm_pin_tec = 5
        self.board.digital[self.pwm_pin_tec].mode = PWM
        
        # relay pin
        self.relay_pin_bfan = 7
        self.relay_pin_sfan = 8

        # temperature pin
        # 1 = plate temp., 0 = heater temp.
        self.tp_pin_t1 = 1
        self.tp_pin_t2 = 0
        self.tp_pin_t3 = 2
        self.tp_pin_t4 = 3
        
        # reset pins
        self.pinOut(self.pwm_pin_heater, 0.0)
        self.pinOut(self.pwm_pin_tec, 0.0)
        self.pinOut(self.relay_pin_bfan, 0.0)
        self.pinOut(self.relay_pin_sfan, 0.0)


    def start(self):
        # setting sampling for temperature
        self.board.analog[self.tp_pin_t1].register_callback(self.PlateTPCallback)
        self.board.analog[self.tp_pin_t2].register_callback(self.TECCoolTPCallback)
        self.board.analog[self.tp_pin_t3].register_callback(self.TECHeatTPCallback)
        #self.board.analog[self.tp_pin_t4].register_callback(self.CameraTPCallback)

        self.board.samplingOn(1000 / self.samplingRate)

        self.board.analog[self.tp_pin_t1].enable_reporting()
        self.board.analog[self.tp_pin_t2].enable_reporting()
        self.board.analog[self.tp_pin_t3].enable_reporting()
        #self.board.analog[self.tp_pin_t4].enable_reporting()

    def PlateTPCallback(self, data):
        # -0.0166
        r2_plate, Tc_plate = self.calT(data)
        #print("Plate TS %f,%f:%f Ohm, %f C" % (self.timestamp_plate, data, r2_plate, Tc_plate))
        self.timestamp_plate += (1 / self.samplingRate)
 
        self.count_plate += 1
        self.temp_plate += Tc_plate

        if self.count_plate == 10:
            self.temp_plate /= 10.0
            print("Plate avg TS %f, %f C" % (self.timestamp_plate, self.temp_plate))
            self.controlFlowForAll(self.temp_plate, self.timestamp_plate)

            self.temp_plate = 0
            self.count_plate = 0


    def TECCoolTPCallback(self, data):
        r2, Tc = self.calT(data)
        #print("TECCool TS %f,%f:%f Ohm, %f C" % (self.timestamp_teccool, data, r2, Tc))
        self.timestamp_teccool += (1 / self.samplingRate)
 
        self.count_teccool += 1
        self.temp_teccool += Tc

        if self.count_teccool == 10:
            self.temp_teccool /= 10.0
            print("TECCool avg TS %f, %f C" % (self.timestamp_teccool, self.temp_teccool))
            self.controlFlowForTECCool(self.temp_teccool, self.timestamp_teccool)

            self.temp_teccool = 0
            self.count_teccool = 0


    def TECHeatTPCallback(self, data):
        r2, Tc = self.calT(data)
        #print("TECHeat TS %f,%f:%f Ohm, %f C" % (self.timestamp_techeat, data, r2, Tc))
        self.timestamp_techeat += (1 / self.samplingRate)
 
        self.count_techeat += 1
        self.temp_techeat += Tc

        if self.count_techeat == 10:
            self.temp_techeat /= 10.0
            print("TECHeat avg TS %f, %f C" % (self.timestamp_techeat, self.temp_techeat))
            self.controlFlowForTECHeat(self.temp_techeat, self.timestamp_teccool)

            self.temp_techeat = 0
            self.count_techeat = 0
        
    def CameraTPCallback(self, data):
        r2, Tc = self.calT(data)
        #print("Camera TS %f,%f:%f Ohm, %f C" % (self.timestamp_camera, data, r2, Tc))
        self.timestamp_camera += (1 / self.samplingRate)
        self.controlFlowForCamera(Tc, self.timestamp_camera)
    
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


    def controlFlowForAll(self, temperature, timestamp):
        '''
            T_low to T_high --> inc_period_time
            stay in T_high --> high_period_time
            T_high to T_low --> dec_period_time
            stay in T_low --> low_period_time
        '''
        '''
            state_high_ts 1 = keep on heating to 95
            state_high_ts 2 = achieve target temperature: 95
            state_high_ts 3 = stop heating, wait cooling to 55
            state_high_ts 4 = achieve target temperature: 55
        '''
        print("state_high_ts = %d" % self.state_high_ts)

        targetPwm = 0.0

        if self.state_high_ts == 1:
            print("state_high_ts = 1")
            '''
                state_high_ts 1 = keep on heating
                use PID
            '''
            
            # stop the cooling and turn off fan
            #self.pinOut(self.pwm_pin_heater, 0.0)
            self.pinOut(self.relay_pin_bfan, 0.0)
            self.pinOut(self.relay_pin_sfan, 0.0)
            
            self.pid_high.update(temperature)
            
            targetPwm = self.pid_high.output
            targetPwm = max(min( targetPwm, 100.0 ), 0.0)
            targetPwm = targetPwm / 100.0
            print("targetPwm = %f" % targetPwm)
            
            self.pinOut(self.pwm_pin_heater, targetPwm)
            # check temperature
            if temperature >= (self.T_high - 5):
                self.last_ts_high = timestamp
                self.state_high_ts = 2
            
        elif self.state_high_ts == 2:
            print("state_high_ts = 2")
            '''
                state_high_ts 2 = achieve target temperature: 95
            '''

            # stop the cooling and turn off fan
            #self.pinOut(self.pwm_pin_heater, 0.0)
            self.pinOut(self.relay_pin_bfan, 0.0)
            self.pinOut(self.relay_pin_sfan, 0.0)

            self.pid_high.update(temperature)
            targetPwm = self.pid_high.output
            targetPwm = max(min( targetPwm, 100.0 ), 0.0)
            targetPwm = targetPwm / 100.0
            self.pinOut(self.pwm_pin_heater, targetPwm)

            # check timestamp
            if (timestamp - self.last_ts_high) >= self.high_pt:
                self.state_high_ts = 3
                self.pinOut(self.pwm_pin_heater, 0.0)
                # change state_low_ts to 3 when state_high_ts about to 3
                # self.state_low_ts = 3
			
			
        elif self.state_high_ts == 3:
            print("state_high_ts = 3")
            '''
                state_high_ts 3 = stop heating
            '''

            # stop the cooling and turn on fan
            self.pinOut(self.pwm_pin_heater, 0.0)
            self.pinOut(self.relay_pin_bfan, 1.0)
            self.pinOut(self.relay_pin_sfan, 1.0)

            if 0:
                tempT = targetLowT - (temperature - targetLowT)
                self.pid_tec.update(tempT)
                targetPwm = self.pid_tec.output
                targetPwm = max(min( targetPwm, 100.0 ), 0.0)
                targetPwm = targetPwm / 100.0
                print("targetPwm = %f" % targetPwm)
                #if b_USE_TEC:
                self.pinOut(self.pwm_pin_tec, targetPwm)
            
            # check temperature
            if temperature <= self.T_low:
                self.last_ts_low = timestamp
                self.pinOut(self.pwm_pin_tec, 0.0)
                self.state_high_ts = 4

        elif self.state_high_ts == 4:
            print("state_high_ts = 4")
            '''
                state_high_ts 4 = achieve target temperature: 55
                stop tec, keep fan
            '''
            #self.pinOut(self.pwm_pin_tec, 0.0)
            self.pinOut(self.relay_pin_bfan, 1.0)
            self.pinOut(self.relay_pin_sfan, 1.0)

            self.pid_low.update(temperature)
            targetPwm = self.pid_low.output
            targetPwm = max(min( targetPwm, 100.0 ), 0.0)
            targetPwm = targetPwm / 100.0
            self.pinOut(self.pwm_pin_heater, targetPwm)

            # check timestamp
            if (timestamp - self.last_ts_low) >= self.low_pt:
                self.state_high_ts = 1
                # change state_low_ts to 3 when state_high_ts about to 3
                # self.state_low_ts = 3

        else:
            '''
                default value
            '''
            # turn off all item
            print("state_high_ts = else")
            self.pinOut(self.pwm_pin_heater, 0.9)
            self.pinOut(self.pwm_pin_tec, 0.0)
            self.pinOut(self.relay_pin_bfan, 0.0)
            self.pinOut(self.relay_pin_sfan, 0.0)

        if self.t1_ofile is not None:
            print("%d\t%f\t%f" % (timestamp, temperature, targetPwm), file=self.t1_ofile)
        return


    def controlFlowForTECCool(self, temperature, timestamp):
        '''
            print the data only
        '''
        if self.t2_ofile is not None:
            print("%d\t%f\t%f" % (timestamp, temperature, 0.0), file=self.t2_ofile)

    def controlFlowForTECHeat(self, temperature, timestamp):
        '''
            print the data only
        '''
        if self.t3_ofile is not None:
            print("%d\t%f\t%f" % (timestamp, temperature, 0.0), file=self.t3_ofile)

    def controlFlowForCamera(self, temperature, timestamp):
        '''
            print the data only
        '''
        if self.t4_ofile is not None:
            print("%d\t%f\t%f" % (timestamp, temperature, targetPwm), file=self.t4_ofile)



t1_path = 't1_output.txt'
t2_path = 't2_output.txt'
t3_path = 't3_output.txt'
t4_path = 't4_output.txt'

try: 
    t1_output_f = open(t1_path, 'w')
    t2_output_f = open(t2_path, 'w')
    t3_output_f = open(t3_path, 'w')
    t4_output_f = open(t4_path, 'w')

    print("Let's print data from Arduino's analog pins for 100secs.")
    # Let's create an instance
    ntc_sensor = CoThermal(t1_ofile=t1_output_f, t2_ofile=t2_output_f, t3_ofile=t3_output_f, t4_ofile=t4_output_f)
    # and start DAQ
    ntc_sensor.start()
    # let's acquire data for 100secs. We could do something else but we just sleep!
    time.sleep(900)
    # let's stop it
    ntc_sensor.stop()
    print("finished")

except:
    print("Unable to create file on disk.")
    t1_output_f.close()
    t2_output_f.close()
    t3_output_f.close()
    t4_output_f.close()

finally:
    t1_output_f.close()
    t2_output_f.close()
    t3_output_f.close()
    t4_output_f.close()


