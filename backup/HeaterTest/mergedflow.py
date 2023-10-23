'''
# command format: ntc100k_sensor.py <time_interval=1>
from argparse import ArgumentParser
parser = ArgumentParser()
# add static parameters
parser.add_argument('led_pin', type=int, help='led pin, display an integer in [0,3]')
parser.add_argument('suffix', type=string, help='file suffix, display a string')
args = parser.parse_args()
'''



from pyfirmata2 import Arduino, PWM
import PID
import time
import math

PORT = 'COM3'
#PORT = Arduino.AUTODETECT


targetHighT = 95
targetLowT = 55
targetEnvT = 30

P = 10
I = 1
D = 1

pid_high = PID.PID(P, I, D)
pid_high.SetPoint = targetHighT
pid_high.setSampleTime(1)

pid_low = PID.PID(P, I, D)
pid_low.SetPoint = targetLowT
pid_low.setSampleTime(1)

pid_env = PID.PID(P, I, D)
pid_env.SetPoint = targetEnvT
pid_env.setSampleTime(1)


class CoThermal:
    '''
        use relay to control heat with Arduino
    '''
    def __init__(self, current_time=None):
        # time
        self.sample_time = 0.00
        self.current_time = current_time if current_time is not None else time.time()
        self.last_time = self.current_time
        

        self.pid_high = pid_high
        self.pid_low = pid_low
        self.pid_env = pid_env

        self.T_low = targetLowT
        self.T_high = targetHighT
        self.T_env = targetEnvT
        self.high_pt = 10000
        self.low_pt = 10000

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
        self.pwm_pin_heater1 = 3
        self.board.digital[self.pwm_pin_heater1].mode = PWM
        self.pwm_pin_heater2 = 5
        self.board.digital[self.pwm_pin_heater2].mode = PWM
        self.pwm_pin_fan = 6
        self.board.digital[self.pwm_pin_fan].mode = PWM
        
        # temperature pin
        self.tp_pin_high = 0
        self.tp_pin_low = 1
        self.tp_pin_env = 2
        
        # relay pin
        self.relay_pin_tec = 7
        self.relay_pin_fan = 8

        # reset pins
        self.pinOut(self.pwm_pin_heater1, 0.0)
        self.pinOut(self.pwm_pin_heater2, 0.0)
        self.pinOut(self.pwm_pin_fan, 0.0)
        self.pinOut(self.relay_pin_fan, 1.0)
        self.pinOut(self.relay_pin_tec, 1.0)



    def start(self):
        # setting sampling for temperature
        self.board.analog[self.tp_pin_high].register_callback(self.HighTPCallback)
        self.board.analog[self.tp_pin_low].register_callback(self.LowTPCallback)
        self.board.analog[self.tp_pin_env].register_callback(self.EnvTPCallback)
        self.board.samplingOn(1000 / self.samplingRate)
        self.board.analog[self.tp_pin_high].enable_reporting()
        self.board.analog[self.tp_pin_low].enable_reporting()
        self.board.analog[self.tp_pin_env].enable_reporting()

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

        elif self.state_high_ts == 3:
            '''
                state_high_ts 3 = stop heating
            '''
            self.pinOut(self.pwm_pin_heater1, 0.0)
            
        else:
            '''
                default value
            '''
            self.pinOut(self.pwm_pin_heater1, 0.0)


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

            if temperature > self.T_low:
                # turn on TEC
                self.pinOut(self.relay_pin_tec, 0.0)
                self.pinOut(self.relay_pin_fan, 0.0)
            else:
                self.pinOut(self.relay_pin_tec, 1.0)
                self.pinOut(self.relay_pin_fan, 1.0)


            # check timestamp
            if (timestamp - self.last_ts_low) >= self.low_pt:
                self.state_low_ts = 3

        elif self.state_low_ts == 3:
            '''
                state_low_ts 3 = stop heating
            '''
            self.pinOut(self.pwm_pin_heater2, 0.0)
            self.pinOut(self.relay_pin_tec, 1.0)
            self.pinOut(self.relay_pin_fan, 1.0)
            
        else:
            '''
                default value
            '''
            self.pinOut(self.pwm_pin_heater2, 0.0)
            self.pinOut(self.relay_pin_tec, 1.0)
            self.pinOut(self.relay_pin_fan, 1.0)

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


print("Let's print data from Arduino's analog pins for 100secs.")
# Let's create an instance
ntc_sensor = CoThermal()
# and start DAQ
ntc_sensor.start()
# let's acquire data for 100secs. We could do something else but we just sleep!
time.sleep(1000)
# let's stop it
ntc_sensor.stop()
print("finished")
