
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

    def resetPCB(self, total_time):
        self.total_time = total_time


    def definePackage(self):
        self.func_OK_package = bytearray(b'')
	
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

    # device functions, TODO: error handling
    def checkOK(self, ret):
        ret_array = ret.split(',')
        if ret_array[3] == 1:
            return True
        if len(ret_array) >= 4:
            return ret_array[-1]
        return False

    # 1: cartridge rotation
    def rotateCart(self, timeout = 10, pos = 0):
        if pos == 0:
            ret = self.sendCmd(timeout, b'1,1,10000,0\n')
            print("Rotate Cartridge to zero position....")
        else:
            ret = self.sendCmd(timeout, b'1,2,%d,0\n' % pos)
            print("Rotate Cartridge to %d position...." % pos)
        return self.checkOK(ret)

    # 2: cup driver
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
    # 5: reverses motor
    # 6: cartridge rotation
    def openDoor(self, timeout = 1):
        ret = self.sendCmd(timeout, b'6,1,1000,0\n')
        print("Open door....")
        return self.checkOK(ret)
    def closeDoor(self, timeout = 1):
        ret = self.sendCmd(timeout, b'6,2,1000,0\n')
        print("Close door....")
        return self.checkOK(ret)

    # 7: Cartridge Roller
    # 8: vertical position
    def moveVertPosTop(self, timeout = 36):
        ret = self.sendCmd(timeout, b'8,1,36000,0\n')
        print("move vertical position to TOP")
        return self.checkOK(ret)
    def moveVertPosMid(self, timeout = 18):
        ret = self.sendCmd(timeout, b'8,2,18000,0\n')
        print("move vertical position to MID")
        return self.checkOK(ret)
    def moveVertPosBtn(self, timeout = 36):
        ret = self.sendCmd(timeout, b'8,3,36000,0\n')
        print("move vertical position to BTN")
        return self.checkOK(ret)

    # 9: BLDC Motor
    def startBLDCMotor(self, timeout = 5, clockwise = True):
        if clockwise == True:
            # clockwise
            ret = self.sendCmd(timeout, b'9,1,100,0\n')
            print("turn on BLDC Motor: clockwise....")
        else:
            # counter clockwise
            ret = self.sendCmd(timeout, b'9,2,100,0\n')
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
        print("turn on Vacuum Air Pump....")
        return self.checkOK(ret)
    def turnOffVacAirPump(self, timeout = 5):
        ret = self.sendCmd(timeout, b'10,2,0,0\n')
        print("turn off Vacuum Air Pump....")
        return self.checkOK(ret)

    # 11: reserves air pump
    # 12: heater
    # 13: reserves heater
    # 14: TEC
    # 15: Water Cooler Fan
    def turnOnWaterFan(self, timeout = 5)
        ret = self.sendCmd(timeout, b'15,1,0,0\n')
        return self.checkOK(ret)
    def turnOffWaterFan(self, timeout = 5)
        ret = self.sendCmd(timeout, b'15,2,0,0\n')
        return self.checkOK(ret)

    # 16: system dissipation fan
    def turnOnSDFan(self, timeout = 5)
        ret = self.sendCmd(timeout, b'16,1,0,0\n')
        return self.checkOK(ret)
    def turnOffSDFan(self, timeout = 5)
        ret = self.sendCmd(timeout, b'16,2,0,0\n')
        return self.checkOK(ret)

    # 17: optical dissipation fan
    def turnOnODFan(self, timeout = 5)
        ret = self.sendCmd(timeout, b'17,1,0,0\n')
        return self.checkOK(ret)
    def turnOffODFan(self, timeout = 5)
        ret = self.sendCmd(timeout, b'17,2,0,0\n')
        return self.checkOK(ret)

    # 20 combo cmd
    def insertCart(self, timeout = 6):
        ret = self.sendCmd(timeout, b'20,2,6000,0\n')
        return self.checkOK(ret)
    def ejectCart(self, timeout = 6):
        ret = self.sendCmd(timeout, b'20,1,6000,0\n')
        return self.checkOK(ret)





if __name__ == "__main__":
    # test QRCodeReader
    qrcr = QRCodeReader()
    qrcr.initPCB()
    ret = qrcr.scan(10)
    print("QRCode scan result: " + ret)
