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
t4 = tube temperature

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
import PID
import time
import math

PORT = 'COM3'
#PORT = Arduino.AUTODETECT

targetHighT = 95
targetLowT = 55

P = 10
I = 1
D = 1

# heater to 95
pid_high = PID.PID(P, I, D)
pid_high.SetPoint = targetHighT
pid_high.setSampleTime(1)

# tec to 55
pid_low = PID.PID(P, I, D)
pid_low.SetPoint = targetLowT
pid_low.setSampleTime(1)

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
        self.sample_time = 0.00
        self.current_time = current_time if current_time is not None else time.time()
        self.last_time = self.current_time
        

        self.pid_high = pid_high
        self.pid_low = pid_low

        self.T_low = targetLowT
        self.T_high = targetHighT
        self.high_pt = 30
        self.low_pt = 30

        self.state_high_ts = 1
        self.state_low_ts = 1
        self.state_env_ts = 1
        
        # temperature sampling rate: 1Hz
        self.samplingRate = 1

        self.timestamp_high = 0
        self.timestamp_low = 0
        self.timestamp_env = 0

        self.last_ts_high = 0
        self.last_ts_low = 0
        self.last_ts_env = 0

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

        # arduino pwm pin, 3 5 6 9 10 11
        self.pwm_pin_heater = 3
        self.board.digital[self.pwm_pin_heater].mode = PWM
        self.pwm_pin_tec = 5
        self.board.digital[self.pwm_pin_tec].mode = PWM
        
        # relay pin
        self.relay_pin_bfan = 7
        self.relay_pin_sfan = 8

        # temperature pin
        self.tp_pin_t1 = 0
        self.tp_pin_t2 = 1
        self.tp_pin_t3 = 2
        self.tp_pin_t4 = 3
        
        # reset pins
        self.pinOut(self.pwm_pin_heater, 0.0)
        self.pinOut(self.pwm_pin_tec, 0.0)
        self.pinOut(self.relay_pin_bfan, 1.0)
        self.pinOut(self.relay_pin_sfan, 1.0)


    def start(self):
        # setting sampling for temperature
        self.board.analog[self.tp_pin_t1].register_callback(self.HighTPCallback)
        self.board.analog[self.tp_pin_t2].register_callback(self.LowTPCallback)
        self.board.analog[self.tp_pin_t3].register_callback(self.LiqTPCallback)
        #self.board.analog[self.tp_pin_t4].register_callback(self.LiqTPCallback)

        self.board.samplingOn(1000 / self.samplingRate)

        self.board.analog[self.tp_pin_t1].enable_reporting()
        self.board.analog[self.tp_pin_t2].enable_reporting()
        self.board.analog[self.tp_pin_t3].enable_reporting()
        #self.board.analog[self.tp_pin_t4].enable_reporting()

    def LowTPCallback(self, data):
        r2, Tc = self.calT(data)
        print("Low TS %f,%f:%f Ohm, %f C" % (self.timestamp_low, data, r2, Tc))
        self.timestamp_low += (1 / self.samplingRate)
        self.controlFlowForLowTS(Tc, self.timestamp_low)

    def EnvTPCallback(self, data):
        r2, Tc = self.calT(data)
        print("Env TS %f,%f:%f Ohm, %f C" % (self.timestamp_env, data, r2, Tc))
        self.timestamp_env += (1 / self.samplingRate)
        self.controlFlowForEnvTS(Tc, self.timestamp_env)

    def LiqTPCallback(self, data):
        r2, Tc = self.calT(data)
        print("Env TS %f,%f:%f Ohm, %f C" % (self.timestamp_env, data, r2, Tc))
        self.timestamp_env += (1 / self.samplingRate)
        self.controlFlowForLiqTS(Tc, self.timestamp_env)

        
    def HighTPCallback(self, data):
        r2, Tc = self.calT(data)
        print("High TS %f,%f:%f Ohm, %f C" % (self.timestamp_high, data, r2, Tc))
        self.timestamp_high += (1 / self.samplingRate)
        self.controlFlowForHighTS(Tc, self.timestamp_high)
    
    def stop(self):
        self.board.samplingOff()
        self.board.exit()
        
    def calT(self, data):
        r2 = self.r1 * ( 1.0/data - 1.0)
        log_r2 = math.log(r2)
        T = (1.0 / (self.c1 + self.c2 * log_r2 + self.c3 * log_r2 * log_r2 * log_r2))
        Tc = T - 273.15
        return r2, Tc

    # pin output
    def pinOut(self, pin, value=1.0):
        print("set digital[%d] value: %f" % (pin, value))
        self.board.digital[pin].write(value)


    def controlFlowForHighTS(self, temperature, timestamp):
        '''
            T_low to T_high --> inc_period_time
            stay in T_high --> high_period_time
            T_high to T_low --> dec_period_time
            stay in T_low --> low_period_time
        '''
        '''
            state_high_ts 1 = keep on heating
            state_high_ts 2 = achieve target temperature
            state_high_ts 3 = stop heating
        '''
        print("state_high_ts = %d" % self.state_high_ts)

        targetPwm = 0.0

        if self.state_high_ts == 1:
            '''
                state_high_ts 1 = keep on heating
                use PID
            '''
            self.pid_high.update(temperature)
            targetPwm = self.pid_high.output
            targetPwm = max(min( targetPwm, 100.0 ), 0.0)
            targetPwm = targetPwm / 100.0
            print("targetPwm = %f" % targetPwm)
            self.pinOut(self.pwm_pin_heater1, targetPwm)
            
            # check temperature
            if temperature >= self.T_high:
                self.last_ts_high = timestamp
                self.state_high_ts = 2
            
        elif self.state_high_ts == 2:
            '''
                state_high_ts 2 = achieve target temperature
            '''
            targetPwm = self.pid_high.output
            targetPwm = max(min( targetPwm, 100.0 ), 0.0)
            targetPwm = targetPwm / 100.0
            self.pinOut(self.pwm_pin_heater1, targetPwm)

            # check timestamp
            if (timestamp - self.last_ts_high) >= self.high_pt:
                self.state_high_ts = 3
                # change state_low_ts to 3 when state_high_ts about to 3
                self.state_low_ts = 3
			
			
        elif self.state_high_ts == 3:
            '''
                state_high_ts 3 = stop heating
            '''
            targetPwm = 0.0
            self.pinOut(self.pwm_pin_heater1, targetPwm)
            
        else:
            '''
                default value
            '''
            targetPwm = 0.0
            self.pinOut(self.pwm_pin_heater1, targetPwm)

        if self.h_output_file is not None:
            print("%d\t%f\t%f" % (timestamp, temperature, targetPwm), file=self.h_output_file)


    def controlFlowForLowTS(self, temperature, timestamp):
        '''
            T_low to T_high --> inc_period_time
            stay in T_high --> high_period_time
            T_high to T_low --> dec_period_time
            stay in T_low --> low_period_time
        '''
        '''
            state_low_ts 1 = keep on heating
            state_low_ts 2 = achieve target temperature
            state_low_ts 3 = stop heating, keep on cooling
        '''
        print("state_low_ts = %d" % self.state_low_ts)

        targetPwm = 0.0

        if self.state_low_ts == 1:
            '''
                state_low_ts 1 = keep on heating
                use PID
            '''
            self.pid_low.update(temperature)
            targetPwm = self.pid_low.output
            targetPwm = max(min( targetPwm, 100.0 ), 0.0)
            targetPwm = targetPwm / 100.0
            print("targetPwm = %f" % targetPwm)
            self.pinOut(self.pwm_pin_heater2, targetPwm)
            self.pinOut(self.relay_pin_tec, 1.0)
            self.pinOut(self.relay_pin_fan, 1.0)
            
            # check temperature
            if temperature >= self.T_low:
                self.high_low_ts = timestamp
                self.state_low_ts = 2
            
        elif self.state_low_ts == 2:
            '''
                state_low_ts 2 = achieve target temperature
            '''
            self.pid_low.update(temperature)
            targetPwm = self.pid_low.output
            targetPwm = max(min( targetPwm, 100.0 ), 0.0)
            targetPwm = targetPwm / 100.0
            self.pinOut(self.pwm_pin_heater2, targetPwm)

            '''
            if temperature > self.T_low:
                # turn on TEC
                self.pinOut(self.relay_pin_tec, 0.0)
                self.pinOut(self.relay_pin_fan, 0.0)
            else:
                self.pinOut(self.relay_pin_tec, 1.0)
                self.pinOut(self.relay_pin_fan, 1.0)
            '''

            # change state_low_ts to 3 when state_high_ts about to 3
            '''
            # check timestamp
            if (timestamp - self.last_ts_low) >= self.low_pt:
                self.state_low_ts = 3
            '''
        elif self.state_low_ts == 3:
            '''
                state_low_ts 3 = stop heating
            '''
            targetPwm = 0.0
            self.pinOut(self.pwm_pin_heater2, targetPwm)
            #self.pinOut(self.relay_pin_tec, 1.0)
            #self.pinOut(self.relay_pin_fan, 1.0)
            
        else:
            '''
                default value
            '''
            targetPwm = 0.0
            self.pinOut(self.pwm_pin_heater2, targetPwm)
            #self.pinOut(self.relay_pin_tec, 1.0)
            #self.pinOut(self.relay_pin_fan, 1.0)

        if self.l_output_file is not None:
            print("%d\t%f\t%f" % (timestamp, temperature, targetPwm), file=self.l_output_file)

    def controlFlowForLiqTS(self, temperature, timestamp):

        if self.e_output_file is not None:
            print("%d\t%f\t0.0" % (timestamp, temperature), file=self.l_output_file)

        return

    def controlFlowForEnvTS(self, temperature, timestamp):
        '''
            T_low to T_high --> inc_period_time
            stay in T_high --> high_period_time
            T_high to T_low --> dec_period_time
            stay in T_low --> low_period_time
        '''
        '''
            state_env_ts 1 = keep on heating
            state_env_ts 2 = achieve target temperature
            state_env_ts 3 = stop heating
        '''
        print("state_env_ts = %d" % self.state_env_ts)
        
        if self.state_env_ts == 1:
            '''
                state_env_ts 1 = if higher than default temperature, turn on fan
                use PID
            '''
            # check temperature
            if temperature >= self.T_env:
                self.pid_env.update(temperature)
                targetPwm = self.pid_env.output
                targetPwm = max(min( targetPwm, 100.0 ), 0.0)
                targetPwm = 1.0 - targetPwm / 100.0
                print("targetPwm = %f" % targetPwm)
                self.pinOut(self.pwm_pin_fan, targetPwm)
            else:
                print("targetPwm = 0.0")
                self.pinOut(self.pwm_pin_fan, 0.0)
            return
            
        else:
            '''
                default value
            '''
            self.pinOut(self.pwm_pin_fan, 0.0)
            return


h_path = 'high_output.txt'
l_path = 'low_output.txt'
e_path = 'env_output.txt'

try: 
    h_output_f = open(h_path, 'w')
    l_output_f = open(l_path, 'w')
    e_output_f = open(e_path, 'w')

    print("Let's print data from Arduino's analog pins for 100secs.")
    # Let's create an instance
    ntc_sensor = CoThermal(h_output_file=h_output_f, l_output_file=l_output_f, e_output_file=e_output_f)
    # and start DAQ
    ntc_sensor.start()
    # let's acquire data for 100secs. We could do something else but we just sleep!
    time.sleep(10000)
    # let's stop it
    ntc_sensor.stop()
    print("finished")

except:
    print("Unable to create file on disk.")
    h_output_f.close()
    l_output_f.close()
    e_output_f.close()
    return

finally:
    h_output_f.close()
    l_output_f.close()
    e_output_f.close()


