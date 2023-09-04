import random, time, string
import numpy as np

class PCRResults:
    def __init__(self, test_id = None, test_name = None, timestamp = None, ct1 = None, ct2 = None, well1_array = None, well2_array = None):
        self.test_id = test_id
        self.test_name = test_name
        self.timestamp = timestamp
        self.ct1 = ct1
        self.ct2 = ct2
        self.well1_array = well1_array
        self.well2_array = well2_array
        self.proc_log = []

        # fake data if all None
        if test_id == None:
            # XXXX-XXXX-XXXX
            temp_string = ''.join(random.choice(string.digits) for x in range(4))  \
                +'-'+''.join(random.choice(string.digits) for x in range(4))       \
                +'-'+''.join(random.choice(string.digits) for x in range(4))
            self.test_id = temp_string

        if test_name == None:
            # XXXXXXXXXXX Test
            temp_string = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10)) + " Test"
            self.test_name = temp_string

        if timestamp == None:
            self.timestamp = time.time()

        if ct1 == None:
            ct = random.randrange(15,25)
            self.ct1 = ct
            self.well1_array = np.append(np.zeros(ct), np.sort(np.random.uniform(0.1, 2, 41-ct)))

        if ct2 == None:
            ct = random.randrange(25,35)
            self.ct2 = ct
            self.well2_array = np.append(np.zeros(ct), np.sort(np.random.uniform(0.1, 2, 41-ct)))

        self.add_log('test id: %s' % self.test_id)
        self.add_log('test name: %s' % self.test_name)
        self.add_log('process at %s' % self.timestamp)


    def add_log(self, log):
        self.proc_log.append(log)
        return

    def reset_log(self):
        self.proc_log = []
        return

