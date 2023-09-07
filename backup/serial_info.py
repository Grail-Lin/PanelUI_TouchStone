
'''
launch program

inital qr code reader
	send 57 00 00 03 04 01 00 00 00 00 00 1F 71 50 41
    recv 31 00 00 03 04 01 00 00 00 00 00 FF F8 50 41

if error, exit

if ok, do while loop for trigger

'''

'''
class PCBConnector:

init:
    1, connect serial
	2, init QRcode Reader

scan:
	parameter: timeout
    1, send scan cmd
	2, wait for qrcode
	3, if timeout, send stop cmd
	3, return failed or scanned text
	
exit:
	1, leave host mode

'''
'''
import time
import serial



class QRCodeReader:

    def __init__(self, port = 'COM10'):
        self.port = port
        self.ser = serial.Serial(port, 115200, timeout=0.050)

        #count = 0
        self.state = 0     # 0 = uninit, 1 = init

        self.init_package = bytearray(b'\x57\x00\x00\x03\x04\x01\x00\x00\x00\x00\x00\x1F\x71\x50\x41')
        self.init_OK_package = bytearray(b'\x31\x00\x00\x03\x04\x01\x00\x00\x00\x00\x00\xFF\xF8\x50\x41')
        self.scan_package = bytearray(b'\x57\x00\x00\x03\x04\x03\x00\x00\x00\x04\x00\x00\x00\x00\x00\xF7\x81\x50\x41')
        self.scan_OK_package = bytearray(b'\x31\x00\x00\x03\x04\x03\x00\x00\x00\x00\x00\xFE\x1A\x50\x41')

        self.stop_package = bytearray(b'\x57\x00\x00\x03\x04\x03\x00\x00\x00\x04\x00\x01\x00\x00\x00\xF6\x7D\x50\x41')

        self.ser.write(self.init_package)
        time.sleep(1)
        while self.ser.in_waiting:
            data = self.ser.readline()
            if (data == self.init_OK_package):
                self.state = 1
                return
            else:
                self.state = 0
                return

    def scan(self, timeout=10):
        # check if initialized
        if self.state == 0:
            return "ERROR: UNINITIALIZED"
        
        # flush the reading data
        if self.ser.in_waiting > 0:
            data = self.ser.readline()

        # send start cmd
        self.ser.write(self.scan_package)
        time.sleep(0.1)
        nowtime = time.time()

        while self.ser.in_waiting < 20:
            time.sleep(0.1)
            difftime = time.time() - nowtime
            if difftime >= timeout:
                ret_string = "ERROR: TIMEOUT"
                self.ser.write(self.stop_package)
                return ret_string


        if self.ser.in_waiting > 19:
            data = self.ser.readline()
            print(data)
            if (data[0:15] == self.scan_OK_package):

                try:
                    ret_string = data[15:].decode("utf-8")
                except:
                    ret_string = "ERROR: DECODED_FAIL"
            else:
                ret_string = "ERROR: SCAN_FAIL"

        else:
            ret_string = "ERROR: TOO_SHORT"
        return ret_string

'''
'''
ListPortInfo

device        COM10
name          COM10
description   ELMO GMAS (COM10)
pid           42151
vid           1317
manufacturer  ELMO LTD.

'''
import os
import sys
import time
import serial
import serial.tools.list_ports

print('Search...')
ports = serial.tools.list_ports.comports(include_links=False)
for port in ports :
    print('Find port '+ port.device)

ser = serial.Serial(port.device)
if ser.isOpen():
    ser.close()

ser = serial.Serial(port.device, 9600, timeout=1)
ser.flushInput()
ser.flushOutput()
print('Connect ' + ser.name)