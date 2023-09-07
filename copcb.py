
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



# basic class
class COPcbConnector:
    def __init__(self, port = None, baudrate = 115200, target_desc = None):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.target_desc = target_desc

        # need to inplement in child class
        self.init_package = None #bytearray(b'\x57\x00\x00\x03\x04\x01\x00\x00\x00\x00\x00\x1F\x71\x50\x41')
        self.init_OK_package = None #bytearray(b'\x31\x00\x00\x03\x04\x01\x00\x00\x00\x00\x00\xFF\xF8\x50\x41')
        self.scan_package = None #bytearray(b'\x57\x00\x00\x03\x04\x03\x00\x00\x00\x04\x00\x00\x00\x00\x00\xF7\x81\x50\x41')
        self.scan_OK_package = None #bytearray(b'\x31\x00\x00\x03\x04\x03\x00\x00\x00\x00\x00\xFE\x1A\x50\x41')
        self.stop_package = None #bytearray(b'\x57\x00\x00\x03\x04\x03\x00\x00\x00\x04\x00\x01\x00\x00\x00\xF6\x7D\x50\x41')

        # return errors
        self.err_uninit = "ERROR: UNINITIALIZED"
        self.err_timeout = "ERROR: TIMEOUT"
        self.err_decode_fail = "ERROR: DECODED_FAIL"
        self.err_func_fail = "ERROR: FUNCTION_FAIL"

        # state
        # 0: uninit
        # 1: init
        self.state = 0
        return

    def __del__(self):
        return

    def connect(self):
        # use description   ELMO GMAS (COM10)
        # to get name       COM10
        # than serial connect it and send inital cmd
        if self.target_desc == None:
            return

        if self.port == None:
            ports = serial.tools.list_ports.comports(include_links=False)
            for port in ports :
                print('Find port '+ port.device + ', desc = ' + port.description)

                if port.description[0:len(self.target_desc)]:
                    self.port = port.device

        if self.port != None:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            self.ser.flushInput()
            self.ser.flushOutput()
            print('Connect ' + self.ser.name)
        return

    # need to inplement in child class
    def definePackage(self):
        return
		
    def initPCB(self, timeout):
        self.definePackage()
        self.ser.write(self.init_package)
        time.sleep(1)
        while self.ser.in_waiting:
            data = self.ser.readline()
            if data == self.init_OK_package:
                self.state = 1
            else:
                self.state = 0
        return

    # need to inplement in child class
    def sendCmd(self, timeout, cmd_str):
        # check if initialized
        if self.state == 0:
            return self.err_uninit
        
        # flush the reading data
        if self.ser.in_waiting > 0:
            data = self.ser.readline()

        # send start cmd
        self.ser.write(cmd_str)
        time.sleep(0.1)
        nowtime = time.time()

        while self.ser.in_waiting <= len(self.scan_OK_package):
            time.sleep(0.1)
            difftime = time.time() - nowtime
            if difftime >= timeout:
                self.ser.write(self.stop_package)
                return self.err_timeout


        if self.ser.in_waiting > len(self.scan_OK_package):
            data = self.ser.readline()
            print(data)
            if (data[0:15] == self.scan_OK_package):
                try:
                    ret_string = data[15:].decode("utf-8")
                except:
                    ret_string = self.err_decode_fail
            else:
                ret_string = self.err_func_fail

        else:
            ret_string = self.err_decode_fail
        return ret_string

    # need to inplement in child class
    #def decode(self, ret_string):
    #    return ret_string

class QRCodeReader(COPcbConnector):
    def __init__(self):
        super().__init__(target_desc = 'ELMO GMAS')
        self.connect()
        self.definePackage()

    def definePackage(self):
        self.init_package = bytearray(b'\x57\x00\x00\x03\x04\x01\x00\x00\x00\x00\x00\x1F\x71\x50\x41')
        self.init_OK_package = bytearray(b'\x31\x00\x00\x03\x04\x01\x00\x00\x00\x00\x00\xFF\xF8\x50\x41')
        self.scan_package = bytearray(b'\x57\x00\x00\x03\x04\x03\x00\x00\x00\x04\x00\x00\x00\x00\x00\xF7\x81\x50\x41')
        self.scan_OK_package = bytearray(b'\x31\x00\x00\x03\x04\x03\x00\x00\x00\x00\x00\xFE\x1A\x50\x41')
        self.stop_package = bytearray(b'\x57\x00\x00\x03\x04\x03\x00\x00\x00\x04\x00\x01\x00\x00\x00\xF6\x7D\x50\x41')
	
    def scan(self, timeout = 10):
        return self.sendCmd(timeout, self.scan_package)

