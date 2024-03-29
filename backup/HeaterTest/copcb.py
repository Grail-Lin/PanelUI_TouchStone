
'''
launch program

inital qr code reader
    send 57 00 00 03 04 01 00 00 00 00 00 1F 71 50 41
    recv 31 00 00 03 04 01 00 00 00 00 00 FF F8 50 41

if error, exit

if ok, do while loop for trigger

'''

import os
import sys
import time
import serial
import serial.tools.list_ports

import random


# basic class
class COPcbConnector:  # BT' baud = 9600
    def __init__(self, port = None, baudrate = 115200, target_desc = None):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.target_desc = target_desc

        # need to inplement in child class
        self.init_package = None #bytearray(b'\x57\x00\x00\x03\x04\x01\x00\x00\x00\x00\x00\x1F\x71\x50\x41')
        self.init_OK_package = None #bytearray(b'\x31\x00\x00\x03\x04\x01\x00\x00\x00\x00\x00\xFF\xF8\x50\x41')
        self.func_package = None #bytearray(b'\x57\x00\x00\x03\x04\x03\x00\x00\x00\x04\x00\x00\x00\x00\x00\xF7\x81\x50\x41')
        self.func_OK_package = None #bytearray(b'\x31\x00\x00\x03\x04\x03\x00\x00\x00\x00\x00\xFE\x1A\x50\x41')
        self.stop_package = None #bytearray(b'\x57\x00\x00\x03\x04\x03\x00\x00\x00\x04\x00\x01\x00\x00\x00\xF6\x7D\x50\x41')

        # return errors
        self.err_uninit = "ERROR: UNINITIALIZED"
        self.err_timeout = "ERROR: TIMEOUT"
        self.err_decode_fail = "ERROR: DECODED_FAIL"
        self.err_func_fail = "ERROR: FUNCTION_FAIL"
        self.code_ok = "OK"

        # state
        # 0: uninit
        # 1: init
        # -1: failed at serial connection
        self.state = 0
        return

    def __del__(self):
        return

    def connect(self):
        # use description   ELMO GMAS (COM10)
        # to get name       COM10
        # than serial connect it and send inital cmd
        if self.target_desc == None and self.port == None:
            self.state = -1
            return

        if self.port == None:
            ports = serial.tools.list_ports.comports(include_links=False)
            for port in ports:
                print('Find port '+ port.device + ', desc = ' + port.description)

                if port.description[0:len(self.target_desc)] == self.target_desc:
                    self.port = port.device

        if self.port != None:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            self.ser.flushInput()
            self.ser.flushOutput()
            print('Connect ' + self.ser.name)
            self.state = 1
        else:
            self.state = -1
        return

    # need to inplement in child class
    def definePackage(self):
        return
        
    def initPCB(self, timeout = 5):
        self.definePackage()
        # check if initialized
        if self.state < 1:
            return self.err_uninit

        self.ser.write(self.init_package)
        time.sleep(1)
        while self.ser.in_waiting:
            data = self.ser.readline()
            if data == self.init_OK_package:
                self.state = 1
            else:
                self.state = 0
        return self.code_ok

    # need to inplement in child class
    def sendCmd(self, timeout, cmd_str):
        # check if initialized
        if self.state < 1:
            return self.err_uninit
        
        # flush the reading data
        if self.ser.in_waiting > 0:
            data = self.ser.readline()

        # send start cmd
        print("CMD String: %s" % str(cmd_str))
        self.ser.write(cmd_str)
        time.sleep(0.1)
        nowtime = time.time()

        while self.ser.in_waiting <= len(self.func_OK_package):
            time.sleep(0.1)
            difftime = time.time() - nowtime
            if difftime >= timeout:
                self.ser.write(self.stop_package)
                return self.err_timeout


        if self.ser.in_waiting > len(self.func_OK_package):
            data = self.ser.read_all()
            #print(data)
            if (data[0:len(self.func_OK_package)] == self.func_OK_package):
                try:
                    ret_string = data[len(self.func_OK_package):].decode("utf-8")
                except:
                    ret_string = self.err_decode_fail
            else:
                ret_string = self.err_func_fail

        else:
            ret_string = self.err_decode_fail
        return ret_string.strip()

    # need to inplement in child class
    #def decode(self, ret_string):
    #    return ret_string

class QRCodeReader(COPcbConnector):
    def __init__(self):
        #super().__init__(target_desc = 'ELMO GMAS')
        super().__init__(target_desc = 'USB')
        self.definePackage()
        self.connect()

    def definePackage(self):
        self.init_package = bytearray(b'\x57\x00\x00\x03\x04\x01\x00\x00\x00\x00\x00\x1F\x71\x50\x41')
        self.init_OK_package = bytearray(b'\x31\x00\x00\x03\x04\x01\x00\x00\x00\x00\x00\xFF\xF8\x50\x41')
        self.func_package = bytearray(b'\x57\x00\x00\x03\x04\x03\x00\x00\x00\x04\x00\x00\x00\x00\x00\xF7\x81\x50\x41')
        self.func_OK_package = bytearray(b'\x31\x00\x00\x03\x04\x03\x00\x00\x00\x00\x00\xFE\x1A\x50\x41')
        self.stop_package = bytearray(b'\x57\x00\x00\x03\x04\x03\x00\x00\x00\x04\x00\x01\x00\x00\x00\xF6\x7D\x50\x41')
    
    def scan(self, timeout = 10):
        return self.sendCmd(timeout, self.func_package)

class QRCodeReaderMock(COPcbConnector):
    def __init__(self):
        #super().__init__(target_desc = 'ELMO GMAS')
        super().__init__(target_desc = 'USB')
        self.definePackage()
        #self.connect()

    def definePackage(self):
        self.init_package = bytearray(b'\x57\x00\x00\x03\x04\x01\x00\x00\x00\x00\x00\x1F\x71\x50\x41')
        self.init_OK_package = bytearray(b'\x31\x00\x00\x03\x04\x01\x00\x00\x00\x00\x00\xFF\xF8\x50\x41')
        self.func_package = bytearray(b'\x57\x00\x00\x03\x04\x03\x00\x00\x00\x04\x00\x00\x00\x00\x00\xF7\x81\x50\x41')
        self.func_OK_package = bytearray(b'\x31\x00\x00\x03\x04\x03\x00\x00\x00\x00\x00\xFE\x1A\x50\x41')
        self.stop_package = bytearray(b'\x57\x00\x00\x03\x04\x03\x00\x00\x00\x04\x00\x01\x00\x00\x00\xF6\x7D\x50\x41')
    
    def scan(self, timeout = 10):
        #return self.sendCmd(timeout, self.func_package)
        return "QRCodeReaderMock"


class ModuleA(COPcbConnector):
    def __init__(self, port = None, target_desc='USB Serial Port'):
        super().__init__(baudrate = 115200, port = port, target_desc = target_desc)
        self.definePackage()
        self.connect()

    def resetPCB(self, total_time):
        self.total_time = total_time


    def definePackage(self):
        self.func_OK_package = bytearray(b'TouchStone HW v0.01 2023.08.18\r\nTouchStone FW v0.01 2023.10.29\r\n')
    
    def doFunc(self, timeout = 10):
        #return self.sendCmd(timeout, self.func_package)
        # return remain_time, other value
        ret = self.total_time
        self.total_time -= 1
        if self.total_time < 0:
            self.total_time = random.randrange(10,180)

    def initPCB(self, timeout = 5):
        self.state = 1
        return

class ModuleBT(COPcbConnector):
    def __init__(self, port = None, target_desc='USB Serial Port'):
        super().__init__(baudrate = 115200, port = port, target_desc = target_desc)
        self.definePackage()
        self.connect()

        self.heaterPhase = 1
        '''
            1 == heat up, use pid1 and pid2
            2 == maintain, use pid2 only
            3 == cooling
            4 == maintain, use pid only
        '''

    def resetPCB(self, total_time):
        self.total_time = total_time


    def definePackage(self):
        self.func_OK_package = bytearray(b'')
    
    def doFunc(self, timeout = 10):
        return

    def initPCB(self, timeout = 5):
        self.state = 1
        print("Log: ModuleBT, initPCB")
        return

    def sendCmd(self, timeout, cmd_str):
        # check if initialized
        if self.state < 1:
            print("Log: the state < 1, error due to uninit")
            return self.err_uninit
        
        # flush the reading data
        if self.ser.in_waiting > 0:
            data = self.ser.readline()

        # send start cmd
        print("CMD String: %s" % str(cmd_str))
        self.ser.write(cmd_str)
        time.sleep(0.1)
        nowtime = time.time()

        while self.ser.in_waiting <= len(self.func_OK_package):
            time.sleep(0.1)
            difftime = time.time() - nowtime
            if difftime >= timeout:
                self.ser.write(self.stop_package)
                return self.err_timeout

        if self.ser.in_waiting > len(self.func_OK_package):
            data = self.ser.read_all()
            #print(data)
            if (data[0:len(self.func_OK_package)] == self.func_OK_package):
                try:
                    ret_string = data[len(self.func_OK_package):].decode("utf-8")
                except:
                    ret_string = self.err_decode_fail
            else:
                ret_string = self.err_func_fail

        else:
            ret_string = self.err_decode_fail
        return ret_string.strip()

    # device functions, TODO: error handling
    def checkOK(self, ret):
        print("Log: return value: %s" % str(ret))
        ret_array = ret.split(',')
        if len(ret_array) == 4 and ret_array[3] == '1':
            return True
        if len(ret_array) >= 4:
            return ret_array[-1]
        return ret_array

    # 1: cartridge rotation
    def rotateCart(self, timeout = 10, pos = 0):
        if pos == 0:
            ret = self.sendCmd(timeout, b'1,1,10000,0\n')
            print("Rotate Cartridge to zero position....")
        else:
            ret = self.sendCmd(timeout, b'1,2,%d,0\n' % pos)
            print("Not Ready: Rotate Cartridge to %d position...." % pos)
        return self.checkOK(ret)

    # 2: cup driver
    def moveCDriver(self, timeout = 3, back = True):
        if back == True:
            ret = self.sendCmd(timeout, b'2,1,3000,0\n')
            print("Move cup driver backward....")
        else:
            ret = self.sendCmd(timeout, b'2,2,3000,0\n')
            print("Move cup driver forward....")
        return self.checkOK(ret)


    # 3: rocker arm
    def moveRArm(self, timeout = 5, release = True):
        if release == True:
            ret = self.sendCmd(timeout, b'3,1,2000,0\n')
            print("Release rocker arm....")
        else:
            ret = self.sendCmd(timeout, b'3,2,2000,0\n')
            print("Contact rocker arm....")
        return self.checkOK(ret)

    # 4: optical position
    def moveOPos(self, timeout = 5, up = True):
        if up == True:
            ret = self.sendCmd(timeout, b'4,1,2000,0\n')
            print("Move optical position up....")
        else:
            ret = self.sendCmd(timeout, b'4,2,2000,0\n')
            print("Move optical position down....")
        return self.checkOK(ret)


    # 5: reverses motor
    # 6: door
    def openDoor(self, timeout = 1):
        ret = self.sendCmd(timeout, b'6,1,1000,0\n')
        print("Open door....")
        return self.checkOK(ret)
    def closeDoor(self, timeout = 1):
        ret = self.sendCmd(timeout, b'6,2,1000,0\n')
        print("Close door....")
        return self.checkOK(ret)

    # 7: Cartridge Roller
    def moveCartRoller(self, timeout = 6, back = True):
        if back == True:
            ret = self.sendCmd(timeout, b'7,1,6000,0\n')
            print("Move cartridge roller backward....")
        else:
            ret = self.sendCmd(timeout, b'7,2,6000,0\n')
            print("Move cartridge roller forward....")
        return self.checkOK(ret)


    # 8: vertical position
    def moveVertPosTop(self, timeout = 36):
        ret = self.sendCmd(timeout, b'8,1,36000,0\n')
        print("move vertical position to TOP")
        return self.checkOK(ret)
    def moveVertPosMid(self, timeout = 18):
        ret = self.sendCmd(timeout, b'8,2,18000,0\n')
        print("move vertical position to MID")
        return self.checkOK(ret)
    def moveVertPosBtm(self, timeout = 36):
        ret = self.sendCmd(timeout, b'8,3,36000,0\n')
        print("move vertical position to BTM")
        return self.checkOK(ret)

    # 9: BLDC Motor
    def startBLDCMotor(self, timeout = 5, clockwise = True):
        if clockwise == True:
            # clockwise
            ret = self.sendCmd(timeout, b'9,1,5000,0\n')
            print("turn on BLDC Motor: clockwise....")
        else:
            # counter clockwise
            ret = self.sendCmd(timeout, b'9,2,5000,0\n')
            print("turn on BLDC Motor: counter clockwise....")
        return self.checkOK(ret)

    def stopBLDCMotor(self, timeout = 5):
        ret = self.sendCmd(timeout, b'9,3,0,0\n')
        print("turn off BLDC Motor....")
        return self.checkOK(ret)

    def setBLDCMotorRPM(self, timeout = 10, rpm = 5000):
        input_rpm = rpm
        if rpm < 3000:
            input_rpm = 3000
        if rpm > 12000:
            input_rpm = 12000

        ret = self.sendCmd(timeout, b'9,5,%d,0\n' % input_rpm)
        print("set BLDC Motor to RPM: %d...." % input_rpm)
        return self.checkOK(ret)

    def readBLDCMotorRPM(self, timeout = 10):
        ret = self.sendCmd(timeout, b'9,4,0,0\n')
        if self.checkOK(ret):
            ret_rpm = ret.strip().split(',')[-2]
            print("read BLDC Motor to RPM: %d...." % ret_rpm)
            return ret_rpm
        print("read BLDC Motor to RPM: failed....")
        return False

    # 10: vacuum air pump
    def turnOnVacAirPump(self, timeout = 5):
        ret = self.sendCmd(timeout, b'10,1,0,0\n')
        print("Not Ready: turn on Vacuum Air Pump....")
        return self.checkOK(ret)
    def turnOffVacAirPump(self, timeout = 5):
        ret = self.sendCmd(timeout, b'10,2,0,0\n')
        print("Not Ready: turn off Vacuum Air Pump....")
        return self.checkOK(ret)

    def setVacAirPump(self, timeout = 5, number = 1, time=100):
        ret = self.sendCmd(timeout, b'10,%d,%d,0\n' % (number+2, time))
        print("Not Ready: set Vacuum Air Pump....")
        return self.checkOK(ret)

    # 11: reserves air pump
    def turnOnRVacAirPump(self, timeout = 5):
        ret = self.sendCmd(timeout, b'11,1,0,0\n')
        print("Not Ready: turn on reserves Vacuum Air Pump....")
        return self.checkOK(ret)

    def turnOffRVacAirPump(self, timeout = 5):
        ret = self.sendCmd(timeout, b'11,2,0,0\n')
        print("Not Ready: turn off reserves Vacuum Air Pump....")
        return self.checkOK(ret)

    def setRVacAirPump(self, timeout = 5, number = 1, time=100):
        ret = self.sendCmd(timeout, b'11,%d,%d,0\n' % (number+2, time))
        print("Not Ready: set reserves Vacuum Air Pump....")
        return self.checkOK(ret)

    # 12: heater, pwm = 0~250
    def turnOnHeater(self, timeout = 5, pwm = 5):
        ret = self.sendCmd(timeout, b'12,1,%d,0\n' % pwm)
        print("turn on Heater, Value = %d...." % pwm)
        return self.checkOK(ret)

    def turnOffHeater(self, timeout = 5):
        ret = self.sendCmd(timeout, b'12,2,0,0\n')
        print("turn off Heater....")
        return self.checkOK(ret)

    def measureSample1(self, timeout = 5):
        ret = self.sendCmd(timeout, b'12,4,0,0\n')
        print("measure sample 1....%s" % str(ret))
        #return self.checkOK(ret)
        try:
            temp = float(ret.split(',')[-1])
            return temp
        except:
            return 0


    # 13: reserves heater
    def turnOnRHeater(self, timeout = 5, pwm = 5):
        ret = self.sendCmd(timeout, b'13,1,%d,0\n' % pwm)
        print("turn on reserves Heater, Value = %d...." % pwm)
        return self.checkOK(ret)

    def turnOffRHeater(self, timeout = 5):
        ret = self.sendCmd(timeout, b'13,2,0,0\n')
        print("turn off reserves Heater....")
        return self.checkOK(ret)

    def measureSample2(self, timeout = 5):
        ret = self.sendCmd(timeout, b'13,4,0,0\n')
        print("measure sample 2....%s" % str(ret))
        #return self.checkOK(ret)
        try:
            temp = float(ret.split(',')[-1])
            return temp
        except:
            return 0

    # 14: TEC
    def turnOnTEC(self, timeout = 5, pwm = 5):
        ret = self.sendCmd(timeout, b'14,1,%d,0\n' % pwm)
        print("turn on TEC, Value = %d...." % pwm)
        return self.checkOK(ret)

    def turnOffTEC(self, timeout = 5):
        ret = self.sendCmd(timeout, b'14,2,0,0\n')
        print("turn off TEC....")
        return self.checkOK(ret)

    def measureTECcold(self, timeout = 5):
        ret = self.sendCmd(timeout, b'14,4,0,0\n')
        print("measure TEC cold side....%s" % str(ret))
        #return self.checkOK(ret)
        try:
            temp = float(ret.split(',')[-1])
            return temp
        except:
            return 0

    def measureTEChot(self, timeout = 5):
        ret = self.sendCmd(timeout, b'14,5,0,0\n')
        print("measure TEC hot side....%s" % str(ret))
        #return self.checkOK(ret)
        try:
            temp = float(ret.split(',')[-1])
            return temp
        except:
            return 0


    # 15: Water Cooler Fan
    def turnOnWaterFan(self, timeout = 5):
        ret = self.sendCmd(timeout, b'15,1,0,0\n')
        print("turn on Water Cooler Fan....")
        return self.checkOK(ret)

    def turnOffWaterFan(self, timeout = 5):
        ret = self.sendCmd(timeout, b'15,2,0,0\n')
        print("turn off Water Cooler Fan....")
        return self.checkOK(ret)

    def turnOnWaterPump(self, timeout = 5):
        ret = self.sendCmd(timeout, b'15,3,0,0\n')
        print("turn on Water Cooler Pump....")
        return self.checkOK(ret)

    def turnOffWaterPump(self, timeout = 5):
        ret = self.sendCmd(timeout, b'15,4,0,0\n')
        print("turn off Water Cooler Pump....")
        return self.checkOK(ret)

    def measureWaterIn(self, timeout = 5):
        ret = self.sendCmd(timeout, b'15,5,0,0\n')
        print("measure WaterIn....%s" % str(ret))
        #return self.checkOK(ret)
        try:
            temp = float(ret.split(',')[-1])
            return temp
        except:
            return 0

    def measureWaterOut(self, timeout = 5):
        ret = self.sendCmd(timeout, b'15,6,0,0\n')
        print("measure WaterOut....%s" % str(ret))
        #return self.checkOK(ret)
        try:
            temp = float(ret.split(',')[-1])
            return temp
        except:
            return 0


    # 16: system dissipation fan
    def turnOnSDFan(self, timeout = 5):
        ret = self.sendCmd(timeout, b'16,1,0,0\n')
        print("turn on System Dissipation Fan....")
        return self.checkOK(ret)
    def turnOffSDFan(self, timeout = 5):
        ret = self.sendCmd(timeout, b'16,2,0,0\n')
        print("turn off System Dissipation Fan....")
        return self.checkOK(ret)

    # 17: optical dissipation fan
    def turnOnODFan(self, timeout = 5):
        ret = self.sendCmd(timeout, b'17,1,0,0\n')
        print("turn on Optical Dissipation Fan....")
        return self.checkOK(ret)

    def turnOffODFan(self, timeout = 5):
        ret = self.sendCmd(timeout, b'17,2,0,0\n')
        print("turn off Optical Dissipation Fan....")
        return self.checkOK(ret)

    # 20 combo cmd
    def insertCart(self, timeout = 60):
        ret = self.sendCmd(timeout, b'20,2,60000,0\n')
        if self.checkOK(ret) == True:
            return True
        else:
            # force insert
            ret = self.forceCloseCart()
            return ret

    def ejectCart(self, timeout = 60):
        ret = self.sendCmd(timeout, b'20,1,60000,0\n')
        return self.checkOK(ret)

    def forceCloseCart(self, timeout = 4):
        ret1 = self.moveCDriver()
        time.sleep(3)
        if ret1 == '1':
            ret2 = self.closeDoor()
            time.sleep(1)
            return ret2
        return ret1

    # turn on heater (1/2/both) for pwm 1~20 (not more than 20), turn off ODFan
    def controlBothHeater(self, timeout = 20, pwm1 = 5, pwm2 = 5):
        # turn off TEC
        #self.turnOffTEC()
        # turn off fans
        #self.turnOffODFan()
        #self.turnOffWaterFan()
        #self.turnOffWaterPump()
        # turn on heater
        if pwm1 > 0:
            self.turnOnHeater(timeout, pwm1)
        else:
            self.turnOffHeater(timeout)

        if pwm2 > 0:
            self.turnOnRHeater(timeout, pwm2)
        else:
            self.turnOffRHeater(timeout)

        return

    def controlPIDBothHeater(self, timeout = 20, pid_p1 = None, pid_p2 = None, p1_target_temp = 130, p2_target_temp = 95, mode = 3):
        # mode = 1 means heater only
        # mode = 2 means r heater only
        # mode = 3 means both heater

        # phase 1, if temp_heater is < p1_target_temp and temp_sample1 < p2_target_temp
        # use pid_1 to calculate pwm for heater
        # phase 2, if temp_heater is >= p1_target_temp or temp_sample1 >= p2_target_temp
        # use pid_2 to calculate pwm for heater

        temp_s1 = self.measureSample1()
        pid_p2.SetPoint = p2_target_temp
        #pid_p2.setSampleTime(0.01)

        if self.heaterPhase == 1:
            temp_h = self.measureTECcold()

            if temp_s1 >= p2_target_temp:
                self.heaterPhase = 2
            elif temp_h >= p1_target_temp:
                self.heaterPhase = 2
            else:
                # use pid_p1
                pid_p1.SetPoint = p1_target_temp
                #pid_p1.setSampleTime(0.01)
                pid_p1.update(temp_h)
                targetPwm = pid_p1.output        
                targetPwm = max(min( targetPwm, 100.0 ), 0.0)
                targetPwm = targetPwm / 100.0
                print("phase 1, targetPwm = %f" % targetPwm)

        
                pwm = 0 # targetPwm
                if mode == 3:
                    pwm1 = pwm
                    pwm2 = pwm
                elif mode == 2:
                    pwm1 = 0
                    pwm2 = pwm
                elif mode == 2:
                    pwm1 = pwm
                    pwm2 = 0
                else:
                    pwm1 = 0
                    pwm2 = 0

                    ret = self.controlBothHeater(timeout, pwm1, pwm2)
                return ret

        # else: # self.heaterPhase == 2 or 4
        # use pid_p2


        # get temp from plate (TEC Cold)
        # todo: calculate PID for pwm/pwm
        pid_p2.update(temp_s1)
        targetPwm = pid_p2.output        
        targetPwm = max(min( targetPwm, 100.0 ), 0.0)
        targetPwm = targetPwm / 100.0
        print("targetPwm = %f" % targetPwm)

        
        pwm = 0 # targetPwm
        if mode == 3:
            pwm1 = pwm
            pwm2 = pwm
        elif mode == 2:
            pwm1 = 0
            pwm2 = pwm
        elif mode == 2:
            pwm1 = pwm
            pwm2 = 0
        else:
            pwm1 = 0
            pwm2 = 0

        ret = self.controlBothHeater(timeout, pwm1, pwm2)

        return ret

    # turn on TEC (turn on the fan, turn off the heater, etc
    def controlPIDTEC(self, timeout = 20, pid = None, target_temp = 4, cool_temp = 40):
        # get temp from sample
        temp = self.measureTECcold()
        # calculate pwm
        pid.SetPoint = target_temp
        #pid.setSampleTime(1)
        temp_tec = target_temp - (temp - target_temp)

        pid.update(temp_tec)
        targetPwm = pid.output        
        targetPwm = max(min( targetPwm, 100.0 ), 0.0)
        targetPwm = targetPwm / 100.0
        print("targetPwm = %f" % targetPwm)

        
        pwm = 0 # targetPwm
        self.turnOnTEC(timeout, pwm)

        # check Water Fan
        self.checkWaterFan(timeout, True, cool_temp)
        return

    # turn off
    # Water Fan is turn on/off by temperature of Water In
    def checkWaterFan(self, timeout = 5, curstate = True, temp = 40):
        # curstate = True means turn on, False means turn off
        # if temp of Water in is higher than target temp, turn on the Fan
        cur_temp = self.measureWaterIn(timeout)    

        if cur_temp > temp:
            self.turnOnWaterFan(timeout)
        else:
            self.turnOffWaterFan(timeout)        
        return

    # System Fan is turn on/off by temperature of PCB
    def checkSystemFan(self, timeout = 5, curstate = True, temp = 40):
        # curstate = True means turn on, False means turn off
        # if temp of System is higher than target temp, turn on the Fan
        cur_temp = self.measureSystem(timeout)

        if cur_temp > temp:
            self.turnOnSDFan(timeout)
        else:
            self.turnOffSDFan(timeout)        
        return

    def measureSystem(self, timeout = 5):
        self.sendCmd(timeout, b'0,1,0,0\n')
        time.sleep(1)
        self.sendCmd(timeout, b'0,3,0,0\n')
        time.sleep(1)
        ret = self.sendCmd(timeout, b'0,5,0,0\n')
        print("measure Temperature of System ....%s" % str(ret))
        #return self.checkOK(ret)
        try:
            temp = float(ret.split(',')[-1])
            return temp
        except:
            return 0



    def controlPIDBothHeater_spec(self, timeout = 20, pid_p1 = None, pid_p2 = None, p1_target_temp = 130, p2_target_temp = 95, mode = 3):
        # mode = 1 means heater only
        # mode = 2 means r heater only
        # mode = 3 means both heater

        # phase 1, if temp_heater is < p1_target_temp and temp_sample1 < p2_target_temp
        # use pid_1 to calculate pwm for heater
        # phase 2, if temp_heater is >= p1_target_temp or temp_sample1 >= p2_target_temp
        # use pid_2 to calculate pwm for heater

        temp_s1 = self.measureSample1()
        time.sleep(2)
        temp_s2 = self.measureSample1()
        time.sleep(2)
        temp_h = self.measureTECcold()
        time.sleep(2)

        pid_p2.SetPoint = p2_target_temp
        #pid_p2.setSampleTime(0.01)

        if self.heaterPhase == 1:
            

            if temp_s1 >= p2_target_temp:
                self.heaterPhase = 2
            elif temp_h >= p1_target_temp:
                self.heaterPhase = 2
            else:
                # use pid_p1
                pid_p1.SetPoint = p1_target_temp
                #pid_p1.setSampleTime(0.01)
                pid_p1.update(temp_h)
                targetPwm = pid_p1.output        
                targetPwm = max(min( targetPwm, 100.0 ), 0.0)
                targetPwm = targetPwm * 20.0/ 100.0
                print("phase 1, targetPwm = %f" % targetPwm)

        
                pwm = targetPwm
                if mode == 3:
                    pwm1 = pwm
                    pwm2 = pwm
                elif mode == 2:
                    pwm1 = 0
                    pwm2 = pwm
                elif mode == 2:
                    pwm1 = pwm
                    pwm2 = 0
                else:
                    pwm1 = 0
                    pwm2 = 0

                    #ret = self.controlBothHeater(timeout, pwm1, pwm2)
                return temp_h, temp_s1, temp_s2, targetPwm

        # else: # self.heaterPhase == 2 or 4
        # use pid_p2


        # get temp from plate (TEC Cold)
        # todo: calculate PID for pwm/pwm
        pid_p2.update(temp_s1)
        targetPwm = pid_p2.output        
        targetPwm = max(min( targetPwm, 100.0 ), 0.0)
        targetPwm = targetPwm * 20.0/ 100.0
        print("targetPwm = %f" % targetPwm)

        
        pwm = targetPwm
        if mode == 3:
            pwm1 = pwm
            pwm2 = pwm
        elif mode == 2:
            pwm1 = 0
            pwm2 = pwm
        elif mode == 2:
            pwm1 = pwm
            pwm2 = 0
        else:
            pwm1 = 0
            pwm2 = 0

        #ret = self.controlBothHeater(timeout, pwm1, pwm2)

        return temp_h, temp_s1, temp_s2, targetPwm

















class ModuleBTMock(COPcbConnector):
    def __init__(self, port = None, target_desc='USB Serial Port'):
        super().__init__(baudrate = 115200, port = port, target_desc = target_desc)
        self.definePackage()
        #self.connect()

    def resetPCB(self, total_time):
        self.total_time = total_time


    def definePackage(self):
        self.func_OK_package = bytearray(b'')
    
    def doFunc(self, timeout = 10):
        return

    def initPCB(self, timeout = 5):
        self.state = 1
        print("Log: ModuleBT (Mock), initPCB")
        return

    def sendCmd(self, timeout, cmd_str):
        print("Log: Mock, sendCmd = %s" % cmd_str)
        return "0,0,0,1"

    # device functions, TODO: error handling
    def checkOK(self, ret):
        print("Log: return value: %s" % str(ret))
        ret_array = ret.split(',')
        if len(ret_array) == 4 and ret_array[3] == '1':
            return True
        if len(ret_array) >= 4:
            return ret_array[-1]
        return ret_array

    # 1: cartridge rotation
    def rotateCart(self, timeout = 10, pos = 0):
        if pos == 0:
            ret = self.sendCmd(timeout, b'1,1,10000,0\n')
            print("Rotate Cartridge to zero position....")
        else:
            ret = self.sendCmd(timeout, b'1,2,%d,0\n' % pos)
            print("Not Ready: Rotate Cartridge to %d position...." % pos)
        return self.checkOK(ret)

    # 2: cup driver
    def moveCDriver(self, timeout = 3, back = True):
        if back == True:
            ret = self.sendCmd(timeout, b'2,1,3000,0\n')
            print("Move cup driver backward....")
        else:
            ret = self.sendCmd(timeout, b'2,2,3000,0\n')
            print("Move cup driver forward....")
        return self.checkOK(ret)


    # 3: rocker arm
    def moveRArm(self, timeout = 5, release = True):
        if release == True:
            ret = self.sendCmd(timeout, b'3,1,2000,0\n')
            print("Release rocker arm....")
        else:
            ret = self.sendCmd(timeout, b'3,2,2000,0\n')
            print("Contact rocker arm....")
        return self.checkOK(ret)

    # 4: optical position
    def moveOPos(self, timeout = 5, up = True):
        if up == True:
            ret = self.sendCmd(timeout, b'4,1,2000,0\n')
            print("Move optical position up....")
        else:
            ret = self.sendCmd(timeout, b'4,2,2000,0\n')
            print("Move optical position down....")
        return self.checkOK(ret)


    # 5: reverses motor
    # 6: door
    def openDoor(self, timeout = 1):
        ret = self.sendCmd(timeout, b'6,1,1000,0\n')
        print("Open door....")
        return self.checkOK(ret)
    def closeDoor(self, timeout = 1):
        ret = self.sendCmd(timeout, b'6,2,1000,0\n')
        print("Close door....")
        return self.checkOK(ret)

    # 7: Cartridge Roller
    def moveCartRoller(self, timeout = 6, back = True):
        if back == True:
            ret = self.sendCmd(timeout, b'7,1,6000,0\n')
            print("Move cartridge roller backward....")
        else:
            ret = self.sendCmd(timeout, b'7,2,6000,0\n')
            print("Move cartridge roller forward....")
        return self.checkOK(ret)


    # 8: vertical position
    def moveVertPosTop(self, timeout = 36):
        ret = self.sendCmd(timeout, b'8,1,36000,0\n')
        print("move vertical position to TOP")
        return self.checkOK(ret)
    def moveVertPosMid(self, timeout = 18):
        ret = self.sendCmd(timeout, b'8,2,18000,0\n')
        print("move vertical position to MID")
        return self.checkOK(ret)
    def moveVertPosBtm(self, timeout = 36):
        ret = self.sendCmd(timeout, b'8,3,36000,0\n')
        print("move vertical position to BTM")
        return self.checkOK(ret)

    # 9: BLDC Motor
    def startBLDCMotor(self, timeout = 5, clockwise = True):
        if clockwise == True:
            # clockwise
            ret = self.sendCmd(timeout, b'9,1,5000,0\n')
            print("turn on BLDC Motor: clockwise....")
        else:
            # counter clockwise
            ret = self.sendCmd(timeout, b'9,2,5000,0\n')
            print("turn on BLDC Motor: counter clockwise....")
        return self.checkOK(ret)

    def stopBLDCMotor(self, timeout = 5):
        ret = self.sendCmd(timeout, b'9,3,0,0\n')
        print("turn off BLDC Motor....")
        return self.checkOK(ret)

    def setBLDCMotorRPM(self, timeout = 10, rpm = 5000):
        input_rpm = rpm
        if rpm < 3000:
            input_rpm = 3000
        if rpm > 12000:
            input_rpm = 12000

        ret = self.sendCmd(timeout, b'9,5,%d,0\n' % input_rpm)
        print("set BLDC Motor to RPM: %d...." % input_rpm)
        return self.checkOK(ret)

    def readBLDCMotorRPM(self, timeout = 10):
        ret = self.sendCmd(timeout, b'9,4,0,0\n')
        if self.checkOK(ret):
            ret_rpm = ret.strip().split(',')[-2]
            print("read BLDC Motor to RPM: %d...." % ret_rpm)
            return ret_rpm
        print("read BLDC Motor to RPM: failed....")
        return False

    # 10: vacuum air pump
    def turnOnVacAirPump(self, timeout = 5):
        ret = self.sendCmd(timeout, b'10,1,0,0\n')
        print("Not Ready: turn on Vacuum Air Pump....")
        return self.checkOK(ret)
    def turnOffVacAirPump(self, timeout = 5):
        ret = self.sendCmd(timeout, b'10,2,0,0\n')
        print("Not Ready: turn off Vacuum Air Pump....")
        return self.checkOK(ret)

    def setVacAirPump(self, timeout = 5, number = 1, time=100):
        ret = self.sendCmd(timeout, b'10,%d,%d,0\n' % (number+2, time))
        print("Not Ready: set Vacuum Air Pump....")
        return self.checkOK(ret)

    # 11: reserves air pump
    def turnOnRVacAirPump(self, timeout = 5):
        ret = self.sendCmd(timeout, b'11,1,0,0\n')
        print("Not Ready: turn on reserves Vacuum Air Pump....")
        return self.checkOK(ret)

    def turnOffRVacAirPump(self, timeout = 5):
        ret = self.sendCmd(timeout, b'11,2,0,0\n')
        print("Not Ready: turn off reserves Vacuum Air Pump....")
        return self.checkOK(ret)

    def setRVacAirPump(self, timeout = 5, number = 1, time=100):
        ret = self.sendCmd(timeout, b'11,%d,%d,0\n' % (number+2, time))
        print("Not Ready: set reserves Vacuum Air Pump....")
        return self.checkOK(ret)

    # 12: heater, pwm = 0~250
    def turnOnHeater(self, timeout = 5, pwm = 5):
        ret = self.sendCmd(timeout, b'12,1,%d,0\n' % pwm)
        print("turn on Heater, Value = %d...." % pwm)
        return self.checkOK(ret)

    def turnOffHeater(self, timeout = 5):
        ret = self.sendCmd(timeout, b'12,2,0,0\n')
        print("turn off Heater....")
        return self.checkOK(ret)

    def measureSample1(self, timeout = 5):
        ret = self.sendCmd(timeout, b'12,4,0,0\n')
        print("measure sample 1....%s" % str(ret))
        #return self.checkOK(ret)
        return float(ret.split(',')[-1])


    # 13: reserves heater
    def turnOnRHeater(self, timeout = 5, pwm = 5):
        ret = self.sendCmd(timeout, b'13,1,%d,0\n' % pwm)
        print("turn on reserves Heater, Value = %d...." % pwm)
        return self.checkOK(ret)

    def turnOffRHeater(self, timeout = 5):
        ret = self.sendCmd(timeout, b'13,2,0,0\n')
        print("turn off reserves Heater....")
        return self.checkOK(ret)

    def measureSample2(self, timeout = 5):
        ret = self.sendCmd(timeout, b'13,4,0,0\n')
        print("measure sample 2....%s" % str(ret))
        #return self.checkOK(ret)
        return float(ret.split(',')[-1])

    # 14: TEC
    def turnOnTEC(self, timeout = 5, pwm = 5):
        ret = self.sendCmd(timeout, b'14,1,%d,0\n' % pwm)
        print("turn on TEC, Value = %d...." % pwm)
        return self.checkOK(ret)

    def turnOffTEC(self, timeout = 5):
        ret = self.sendCmd(timeout, b'14,2,0,0\n')
        print("turn off TEC....")
        return self.checkOK(ret)

    def measureTECcold(self, timeout = 5):
        ret = self.sendCmd(timeout, b'14,4,0,0\n')
        print("measure TEC cold side....%s" % str(ret))
        #return self.checkOK(ret)
        return float(ret.split(',')[-1])

    def measureTEChot(self, timeout = 5):
        ret = self.sendCmd(timeout, b'14,5,0,0\n')
        print("measure TEC hot side....%s" % str(ret))
        #return self.checkOK(ret)
        return float(ret.split(',')[-1])


    # 15: Water Cooler Fan
    def turnOnWaterFan(self, timeout = 5):
        ret = self.sendCmd(timeout, b'15,1,0,0\n')
        print("turn on Water Cooler Fan....")
        return self.checkOK(ret)

    def turnOffWaterFan(self, timeout = 5):
        ret = self.sendCmd(timeout, b'15,2,0,0\n')
        print("turn off Water Cooler Fan....")
        return self.checkOK(ret)

    def turnOnWaterPump(self, timeout = 5):
        ret = self.sendCmd(timeout, b'15,3,0,0\n')
        print("turn on Water Cooler Pump....")
        return self.checkOK(ret)

    def turnOffWaterPump(self, timeout = 5):
        ret = self.sendCmd(timeout, b'15,4,0,0\n')
        print("turn off Water Cooler Pump....")
        return self.checkOK(ret)

    def measureWaterIn(self, timeout = 5):
        ret = self.sendCmd(timeout, b'15,5,0,0\n')
        print("measure WaterIn....%s" % str(ret))
        #return self.checkOK(ret)
        return float(ret.split(',')[-1])

    def measureWaterOut(self, timeout = 5):
        ret = self.sendCmd(timeout, b'15,6,0,0\n')
        print("measure WaterOut....%s" % str(ret))
        #return self.checkOK(ret)
        return float(ret.split(',')[-1])


    # 16: system dissipation fan
    def turnOnSDFan(self, timeout = 5):
        ret = self.sendCmd(timeout, b'16,1,0,0\n')
        print("turn on System Dissipation Fan....")
        return self.checkOK(ret)
    def turnOffSDFan(self, timeout = 5):
        ret = self.sendCmd(timeout, b'16,2,0,0\n')
        print("turn off System Dissipation Fan....")
        return self.checkOK(ret)

    # 17: optical dissipation fan
    def turnOnODFan(self, timeout = 5):
        ret = self.sendCmd(timeout, b'17,1,0,0\n')
        print("turn on Optical Dissipation Fan....")
        return self.checkOK(ret)

    def turnOffODFan(self, timeout = 5):
        ret = self.sendCmd(timeout, b'17,2,0,0\n')
        print("turn off Optical Dissipation Fan....")
        return self.checkOK(ret)

    # 20 combo cmd
    def insertCart(self, timeout = 60):
        ret = self.sendCmd(timeout, b'20,2,60000,0\n')
        if self.checkOK(ret) == True:
            return True
        else:
            # force insert
            ret = self.forceCloseCart()
            return ret

    def ejectCart(self, timeout = 60):
        ret = self.sendCmd(timeout, b'20,1,60000,0\n')
        return self.checkOK(ret)

    def forceCloseCart(self, timeout = 4):
        ret1 = self.moveCDriver()
        time.sleep(3)
        if ret1 == '1':
            ret2 = self.closeDoor()
            time.sleep(1)
            return ret2
        return ret1

    # turn on heater (1/2/both) for pwm 1~20 (not more than 20), turn off ODFan
    def controlBothHeater(self, timeout = 20, pwm1 = 5, pwm2 = 5):
        # turn off TEC
        #self.turnOffTEC()
        # turn off fans
        #self.turnOffODFan()
        #self.turnOffWaterFan()
        #self.turnOffWaterPump()
        # turn on heater
        if pwm1 > 0:
            self.turnOnHeater(timeout, pwm1)
        else:
            self.turnOffHeater(timeout, pwm1)

        if pwm2 > 0:
            self.turnOnRHeater(timeout, pwm2)
        else:
            self.turnOffRHeater(timeout, pwm2)

        return

    def controlPIDBothHeater(self, timeout = 20, pid = None, target_temp = 95, mode = 3):
        # mode = 1 means heater only
        # mode = 2 means r heater only
        # mode = 3 means both heater
        # get temp from plate (TEC Cold)
        temp = self.measureTECcold()
        # todo: calculate PID for pwm/pwm
        
        pwm = 0
        if mode == 3:
            pwm1 = pwm
            pwm2 = pwm
        elif mode == 2:
            pwm1 = 0
            pwm2 = pwm
        elif mode == 2:
            pwm1 = pwm
            pwm2 = 0
        else:
            pwm1 = 0
            pwm2 = 0

        ret = self.controlBothHeater(timeout, pwm1, pwm2)

        return ret

    # turn on TEC (turn on the fan, turn off the heater, etc
    def controlPIDTEC(self, timeout = 20, pid = None, target_temp = 4, cool_temp = 40):
        # get temp from sample
        temp = self.measureTECcold()
        # calculate pwm
        pwm = 0
        self.turnOnTEC(timeout, pwm)

        # check Water Fan
        self.checkWaterFan(timeout, True, cool_temp)
        return

    # turn off
    # Water Fan is turn on/off by temperature of Water In
    def checkWaterFan(self, timeout = 5, curstate = True, temp = 40):
        # curstate = True means turn on, False means turn off
        # if temp of Water in is higher than target temp, turn on the Fan
        cur_temp = self.measureWaterIn(timeout)    

        if cur_temp > temp:
            self.turnOnWaterFan(timeout)
        else:
            self.turnOffWaterFan(timeout)        
        return

    # System Fan is turn on/off by temperature of PCB
    def checkSystemFan(self, timeout = 5, curstate = True, temp = 40):
        # curstate = True means turn on, False means turn off
        # if temp of System is higher than target temp, turn on the Fan
        cur_temp = self.measureSystem(timeout)

        if cur_temp > temp:
            self.turnOnSDFan(timeout)
        else:
            self.turnOffSDFan(timeout)        
        return

    def measureSystem(self, timeout = 5):
        ret = self.sendCmd(timeout, b'0,5,0,0\n')
        print("measure Temperature of System ....%s" % str(ret))
        #return self.checkOK(ret)
        return float(ret.split(',')[-1])

    def controlPIDBothHeater_spec(self, timeout = 20, pid_p1 = None, pid_p2 = None, p1_target_temp = 130, p2_target_temp = 95, mode = 3):
        temp_h = 3
        temp_s1 = 4.5
        temp_s2 = 5.5
        targetPwm = 0.2
        return temp_h, temp_s1, temp_s2, targetPwm



if __name__ == "__main__":
    # test QRCodeReader
    qrcr = QRCodeReader()
    qrcr.initPCB()
    ret = qrcr.scan(10)
    print("QRCode scan result: " + ret)
