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
'''
流程:

initial:
	pin1: register_callback(heaterTP1)
	pin2: register_callback(plate1TP1)
	pin3: register_callback(plate2TP1)

stage 1>2:
	pin1: unregister_callback
	pin2: unregister_callback

	pin1: register_callback(heaterTP2)
	pin2: register_callback(plate1TP2)

stage 2>3:
	pin2: unregister_callback

	pin2: register_callback(plate1TP3)

stage 3>4:
	pin2: unregister_callback

	pin2: register_callback(plate1TP4)

stage 4>1:
	pin1: unregister_callback
	pin2: unregister_callback

	pin1: register_callback(heaterTP1)
	pin2: register_callback(plate1TP1)




1, 升溫時, stage = 1
用 heater temp control PID1
PID1 target = 95




2, 維持高溫, stage = 2
用 plate av temp control PID2
PID2 target = 95

3, 降溫時, stage = 3
用 heater temp control PID3
PID3 target = 55

4, 維持低溫, stage = 4
用 plate av temp control PID4
PID4 target = 55


callback1-1: heaterTP1 --- use heaterTP+PID1(95) to count V for heater, when TP >= 95, stage1>2
callback2-1: plate1TP1 --- record plate1TP
callback3-1: plate2TP1 --- record plate2TP

callback1-2: heaterTP2 --- record heaterTP
callback2-2: plate1TP2 --- use plate1TP+PID2(95) to count V for heater, when time > enough, stage2>3
*callback3-2: plate2TP1 --- record plate2TP

*callback1-3: heaterTP2 --- record heaterTP
callback2-3: plate1TP3 --- record plate1TP, when TP <= 55, stage3>4
*callback3-3: plate2TP1 --- record plate2TP

*callback1-4: heaterTP2 --- record heaterTP
callback2-4: plate1TP4 --- use plate1TP+PID3(55) to count V for heater, when time > enough, stage4>1
*callback3-4: plate2TP1 --- record plate2TP

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
targetHighT = 95
targetLowT = 55
ptHighT = 30
ptLowT = 30

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

PID1_Kp = 10
PID1_Ki = 1
PID1_Kd = 1

PID2_Kp = 9.1
PID2_Ki = 0.3
PID2_Kd = 1.8

PID3_Kp = 9.1
PID3_Ki = 0.3
PID3_Kd = 1.8

# pid1: target = 95, use heater temp to control
pid1 = PID(PID1_Kp, PID1_Ki, PID1_Kd)
pid1.SetPoint = targetHighT
pid1.setSampleTime(0.1)

# pid2: target = 95, use plate temp to control
pid2 = PID(PID2_Kp, PID2_Ki, PID2_Kd)
pid2.SetPoint = targetHighT
pid2.setSampleTime(0.1)

# pid3: target = 55, use plate temp to control
pid3 = PID(PID3_Kp, PID3_Ki, PID3_Kd)
pid3.SetPoint = targetLowT
pid3.setSampleTime(0.1)



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
        self.pid3 = pid3

        self.T_low = targetLowT
        self.T_high = targetHighT
        self.high_pt = ptHighT
        self.low_pt = ptLowT

        self.state_high_ts = 1
        
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
        self.pwm_pin_heater = 3
        self.board.digital[self.pwm_pin_heater].mode = PWM
        #self.pwm_pin_tec = 5
        #self.board.digital[self.pwm_pin_tec].mode = PWM
        
        # relay pin
        #self.relay_pin_bfan = 7
        #self.relay_pin_sfan = 8

        # temperature pin
        # 1 = plate temp., 0 = heater temp.
        self.tp_pin_t1 = 0
        self.tp_pin_t2 = 1
        self.tp_pin_t3 = 2
        
        # reset pins
        self.pinOut(self.pwm_pin_heater, 0.0)
        #self.pinOut(self.pwm_pin_tec, 0.0)
        #self.pinOut(self.relay_pin_bfan, 0.0)
        #self.pinOut(self.relay_pin_sfan, 0.0)


    def start(self):
        # setting sampling for temperature
        self.board.analog[self.tp_pin_t1].register_callback(self.heaterTP1Callback)
        self.board.analog[self.tp_pin_t2].register_callback(self.plate1TP1Callback)
        self.board.analog[self.tp_pin_t3].register_callback(self.plate2TP1Callback)

        self.board.samplingOn(1000 / self.samplingRate)

        self.board.analog[self.tp_pin_t1].enable_reporting()
        self.board.analog[self.tp_pin_t2].enable_reporting()
        self.board.analog[self.tp_pin_t3].enable_reporting()

    # heaterTP1 cb, use heaterTP + PID1 to count V_heater, when TP>=95, stage1->2
    def heaterTP1Callback(self, data):
        r2, Tc = self.calT(data)
        #print("Plate TS %f,%f:%f Ohm, %f C" % (self.timestamp_heater, data, r2, Tc))
        self.timestamp_heater += (1 / self.samplingRate)
 
        self.count_heater += 1
        self.temp_heater += Tc

        if self.count_heater == 10:
            self.temp_heater /= 10.0
            print("Heater avg TS %f, %f C" % (self.timestamp_heater, self.temp_heater))
            self.controlFlowPrintTPOnly(self.t1_ofile, self.temp_heater, self.timestamp_heater)

            if self.state_high_ts == 1:
                # use heater temp to control PID1
                self.controlFlowForPID(self.pid1, self.temp_heater)

                # check temperature >= high?
                if self.temp_heater >= self.T_high:
                    self.state_high_ts = 2
                    print("temperature > highTP, state_high_ts = 2")
                    self.last_ts_high = self.timestamp_heater

                    #self.board.analog[self.tp_pin_t1].unregister_callback()
                    #self.board.analog[self.tp_pin_t2].unregister_callback()

                    #self.board.analog[self.tp_pin_t1].register_callback(self.heaterTP2Callback)
                    #self.board.analog[self.tp_pin_t2].register_callback(self.plate1TP2Callback)

            #elif self.state_high_ts == 2:
            #elif self.state_high_ts == 3:
            #elif self.state_high_ts == 4:
            #else:    # state_high_ts = 2/3/4, do nothing

            # reset temp and count
            self.temp_heater = 0
            self.count_heater = 0

        return


    # plate1TP1 cb, record only
    def plate1TP1Callback(self, data):
        r2, Tc = self.calT(data)
        #print("TECHeat TS %f,%f:%f Ohm, %f C" % (self.timestamp_plate2, data, r2, Tc))
        self.timestamp_plate1 += (1 / self.samplingRate)
 
        self.count_plate1 += 1
        self.temp_plate1 += Tc

        if self.count_plate1 == 10:
            self.temp_plate1 /= 10.0
            print("Plate1 avg TS %f, %f C" % (self.timestamp_plate1, self.temp_plate1))
            self.controlFlowPrintTPOnly(self.t2_ofile, self.temp_plate1, self.timestamp_plate1)

            #if self.state_high_ts == 1:
            # do nothing
            if self.state_high_ts == 2:
                self.controlFlowForPID(self.pid2, self.temp_plate1)

                if (self.timestamp_plate1 - self.last_ts_high) >= self.high_pt:
                    self.state_high_ts = 3
                    print("time period long enough, state_high_ts = 3")
                    self.pinOut(self.pwm_pin_heater, 0.0)

                    #self.board.analog[self.tp_pin_t2].unregister_callback()
                    #self.board.analog[self.tp_pin_t2].register_callback(self.plate1TP3Callback)

            elif self.state_high_ts == 3:
                if self.temp_plate1 <= T_low:
                    self.state_high_ts = 4
                    print("temperature <= lowT, state_high_ts = 4")
                    self.last_ts_low = self.timestamp_plate1

            elif self.state_high_ts == 4:
                self.controlFlowForPID(self.pid3, self.temp_plate1)

                if (self.timestamp_plate1 - self.last_ts_low) >= self.low_pt:
                    self.state_high_ts = 1
                    print("time period long enough, state_high_ts = 1")
                    #self.board.analog[self.tp_pin_t1].unregister_callback()
                    #self.board.analog[self.tp_pin_t2].unregister_callback()

                    #self.board.analog[self.tp_pin_t1].register_callback(self.heaterTP1Callback)
                    #self.board.analog[self.tp_pin_t2].register_callback(self.plate1TP1Callback)

            # reset temp and count
            self.temp_plate1 = 0
            self.count_plate1 = 0

        return

    # plate2TP1 cb, record only
    def plate2TP1Callback(self, data):
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

    # heaterTP2 cb, record only
    '''
    def heaterTP2Callback(self, data):
        r2, Tc = self.calT(data)
        #print("TECHeat TS %f,%f:%f Ohm, %f C" % (self.timestamp_plate2, data, r2, Tc))
        self.timestamp_heater += (1 / self.samplingRate)
 
        self.count_heater += 1
        self.temp_heater += Tc

        if self.count_heater == 10:
            self.temp_heater /= 10.0
            print("Heater avg TS %f, %f C" % (self.timestamp_heater, self.temp_heater))
            self.controlFlowPrintTPOnly(self.t1_ofile, self.temp_heater, self.timestamp_heater)

            self.temp_heater = 0
            self.count_heater = 0
        return
    
    
    # plate1TP2 cb, use plate1TP + PID2 to count V_heater, when time > pt, stage2->3
    def plate1TP2Callback(self, data):
        r2, Tc = self.calT(data)
        #print("Plate TS %f,%f:%f Ohm, %f C" % (self.timestamp_heater, data, r2, Tc))
        self.timestamp_plate1 += (1 / self.samplingRate)
 
        self.count_plate1 += 1
        self.temp_plate1 += Tc

        if self.count_plate1 == 10:
            self.temp_plate1 /= 10.0
            print("Plate avg TS %f, %f C" % (self.timestamp_plate1, self.temp_plate1))
            self.controlFlowPrintTPOnly(self.t2_ofile, self.temp_plate1, self.timestamp_plate1)

            if self.state_high_ts == 2:
                self.controlFlowForPID(self.pid2, self.temp_plate1)

                if (self.timestamp_plate1 - self.last_ts_high) >= self.high_pt:
                    self.state_high_ts = 3
                    print("state_high_ts = 3")
                    self.pinOut(self.pwm_pin_heater, 0.0)

                    #self.board.analog[self.tp_pin_t2].unregister_callback()
                    #self.board.analog[self.tp_pin_t2].register_callback(self.plate1TP3Callback)

            elif self.state_high_ts == 3:
                if self.temp_plate1 <= T_low:
                    self.state_high_ts = 4
                    print("state_high_ts = 4")
                    self.last_ts_low = self.timestamp_plate1

            elif self.state_high_ts == 4:
                self.controlFlowForPID(self.pid3, self.temp_plate1)

                if (self.timestamp_plate1 - self.last_ts_low) >= self.low_pt:
                    self.state_high_ts = 1
                    print("state_high_ts = 1")
                    self.board.analog[self.tp_pin_t1].unregister_callback()
                    self.board.analog[self.tp_pin_t2].unregister_callback()

                    self.board.analog[self.tp_pin_t1].register_callback(self.heaterTP1Callback)
                    self.board.analog[self.tp_pin_t2].register_callback(self.plate1TP1Callback)



            # reset temp and count
            self.temp_plate1 = 0
            self.count_plate1 = 0

        return
    '''
    # plate1TP3 cb, record only, when TP <= lowT, stage3->4
    # plate1TP4 cb, use plate1TP + PID3 to count V_heater, when time > pt, stage4->1





    '''
    def PlateTPCallback(self, data):
        # -0.0166
        r2_plate, Tc_plate = self.calT(data)
        #print("Plate TS %f,%f:%f Ohm, %f C" % (self.timestamp_heater, data, r2_plate, Tc_plate))
        self.timestamp_heater += (1 / self.samplingRate)
 
        self.count_heater += 1
        self.temp_heater += Tc_plate

        if self.count_heater == 10:
            self.temp_heater /= 10.0
            print("Plate avg TS %f, %f C" % (self.timestamp_heater, self.temp_heater))
            self.controlFlowForAll(self.temp_heater, self.timestamp_heater)

            self.temp_heater = 0
            self.count_heater = 0


    def TECCoolTPCallback(self, data):
        r2, Tc = self.calT(data)
        #print("TECCool TS %f,%f:%f Ohm, %f C" % (self.timestamp_plate1, data, r2, Tc))
        self.timestamp_plate1 += (1 / self.samplingRate)
 
        self.count_plate1 += 1
        self.temp_plate1 += Tc

        if self.count_plate1 == 10:
            self.temp_plate1 /= 10.0
            print("TECCool avg TS %f, %f C" % (self.timestamp_plate1, self.temp_plate1))
            self.controlFlowForTECCool(self.temp_plate1, self.timestamp_plate1)

            self.temp_plate1 = 0
            self.count_plate1 = 0


    def TECHeatTPCallback(self, data):
        r2, Tc = self.calT(data)
        #print("TECHeat TS %f,%f:%f Ohm, %f C" % (self.timestamp_plate2, data, r2, Tc))
        self.timestamp_plate2 += (1 / self.samplingRate)
 
        self.count_plate2 += 1
        self.temp_plate2 += Tc

        if self.count_plate2 == 10:
            self.temp_plate2 /= 10.0
            print("TECHeat avg TS %f, %f C" % (self.timestamp_plate2, self.temp_plate2))
            self.controlFlowForTECHeat(self.temp_plate2, self.timestamp_plate1)

            self.temp_plate2 = 0
            self.count_plate2 = 0
        
    def CameraTPCallback(self, data):
        r2, Tc = self.calT(data)
        #print("Camera TS %f,%f:%f Ohm, %f C" % (self.timestamp_camera, data, r2, Tc))
        self.timestamp_camera += (1 / self.samplingRate)
        self.controlFlowForCamera(Tc, self.timestamp_camera)
    '''

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
    def controlFlowPrintTPOnly(self, t_ofile, temperature, timestamp):
        '''
            print the data only
        '''
        if t_ofile is not None:
            print("%d\t%f\t%f" % (timestamp, temperature, 0.0), file=t_ofile)

        return

    def controlFlowForPID(self, current_pid, temperature):
        current_pid.update(temperature)

        targetPwm = current_pid.output
        targetPwm = max(min( targetPwm, 100.0 ), 0.0)
        targetPwm = targetPwm / 100.0
        print("targetPwm = %f" % targetPwm)

        self.pinOut(self.pwm_pin_heater, targetPwm)

        return



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
    time.sleep(900)
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


