'''
# command format: read_pd.py <pwn=0-1> <time=10>
from argparse import ArgumentParser
parser = ArgumentParser()
# add static parameters
parser.add_argument('voltage', type=float, help='led voltage power, [0-5]')
parser.add_argument('time', type=int, help='time for led period')
args = parser.parse_args()
'''
'''
initial: 
send 57 00 00 03 04 01 00 00 00 00 00 1F 71 50 41
recv 31 00 00 03 04 01 00 00 00 00 00 FF F8 50 41

send 57 00 00 03 04 03 00 00 00 04 00 00 00 00 00 F7 81 50 41
recv 31 00 00 03 04 03 00 00 00 00 00 FE 1A 50 41


stop decoding:
send 57 00 00 03 04 03 00 00 00 04 00 01 00 00 00 F6 7D 50 41

Aztec Code Test = 
41 7A 74 65 63 20 43 6F 64 65 20 54 65 73 74 0D
'''

'''
launch program

inital qr code reader
	send 57 00 00 03 04 01 00 00 00 00 00 1F 71 50 41
    recv 31 00 00 03 04 01 00 00 00 00 00 FF F8 50 41

if error, exit

if ok, do while loop for trigger

'''

'''
class QRcodeReader:

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

        '''
        while self.ser.in_waiting:
            data = self.ser.readline()
            if (data == self.scan_OK_package):
                while self.ser.in_waiting:
                    ret_string = self.ser.readline().decode("utf-8")
            else:
                ret_string = "ERROR: SCAN_FAIL"
        return ret_string
        '''
        return ret_string

'''
while 1:
    if(state == 0):          //waits for incoming data
        while ser.in_waiting:
            data = ser.readline().decode("ascii")
            if(data == '1')  //received a '1' move onto next state
                state = 1;
                print("1 received")
                ser.write("1 received").encode()
            else:           //wrong data stay at state 0
                print("back to the start")
                ser.write("back to the start").encode()

    elif(state == 1):          //waits for incoming data
        while ser.in_waiting:
            data = ser.readline().decode("ascii")
            if(data == '2')  //received a '2' move on to next state
                state = 2;
                print("2 received")
                ser.write("2 received").encode()
            else:            //wrong data return to state 0  
                state = 0;
                print("back to the start")
                ser.write("back to the start").encode()

    elif(state == 2):          //waits for incoming data
        while ser.in_waiting:
            data = ser.readline().decode("ascii")
            if(data == '3')  //received a '3'  //received a '3' print message
                print("You win!")
                ser.write("You win!").encode()
                state = 0; 
            else:             //wrong data return to state 0  
                state = 0;
                print("back to the start")
                ser.write("back to the start").encode()

'''