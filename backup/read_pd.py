
# command format: read_pd.py <pwn=0-1> <time=10>
from argparse import ArgumentParser
parser = ArgumentParser()
# add static parameters
parser.add_argument('voltage', type=float, help='led voltage power, [0-5]')
parser.add_argument('-t', '--time', type=int, default=3, help='time for led period')
parser.add_argument('-f', '--filepath', type=str, default=None, help='filepath for output data')

args = parser.parse_args()

'''
trigger led voltage = pwn for time = time
read analog input from pin
'''



from pyfirmata2 import Arduino, PWM
import time
import math

#PORT = 'COM3'
PORT = Arduino.AUTODETECT


class PDReader:
    '''
        triger led voltage = pwm for time = time
        read analog input from pin
    '''
    def __init__(self, pwm=1, output_file=None):
        
        # output file
        self.output_file = output_file if output_file is not None else None

        # time
        self.sample_time = 0.00
        self.current_time = time.time()
        self.last_time = self.current_time

        self.pwm = pwm
        
        # sampling rate: 100Hz (100次/1秒)
        self.samplingRate = 100

        self.timestamp_pone = 0

        self.board = Arduino(PORT)

        # arduino pwm pin, 3 5 6 9 10 11
        self.pwm_pin = 3
        self.board.digital[self.pwm_pin].mode = PWM
        
        # read pin, 0
        self.pd_pin = 0

        # reset pins
        self.pinOut(self.pwm_pin, 0.0)


    def start(self):
        # setting sampling for temperature
        self.pinOut(self.pwm_pin, self.pwm)
        self.board.analog[self.pd_pin].register_callback(self.PDreadCallback)
        self.board.samplingOn(1000 / self.samplingRate)
        self.board.analog[self.pd_pin].enable_reporting()

    def PDreadCallback(self, data):
        data = self.calT(data)
        print("Timestamp: %f, PD_READER: %f" % (self.timestamp_pone, data))

        if self.output_file is not None:
            print("%f\t%f" % (self.timestamp_pone, data), file=self.output_file)


        self.timestamp_pone += (1 / self.samplingRate)


    
    def stop(self):
        self.board.samplingOff()
        self.pinOut(self.pwm_pin, 0.0)
        self.board.exit()
        
    def calT(self, data):
        ret = 5.0*data
        return ret

    # pin output
    def pinOut(self, pin, value=1.0):
        print("set digital[%d] value: %f" % (pin, value))
        self.board.digital[pin].write(value)



try: 

    if args.filepath != None:
        output_f = open(args.filepath, 'w')
    else:
        output_f = None

    print("Let's print data from Arduino's analog pins for N secs.")
    # Let's create an instance
    value = args.voltage / 5.0

    if args.voltage < 0.0:
        value = 0
    if args.voltage >= 5.0:
        value = 1.0

    pd_sensor = PDReader(pwm=value, output_file = output_f)
    # and start DAQ
    pd_sensor.start()
    # let's acquire data for 100secs. We could do something else but we just sleep!
    time.sleep(args.time)
    # let's stop it
    pd_sensor.stop()
    print("finished")

except Exception as e:
    print(e)
    if args.filepath != None:
        output_f.close()

finally:
    if args.filepath != None:
        output_f.close()


