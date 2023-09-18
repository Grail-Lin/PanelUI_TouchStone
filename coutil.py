import random, time, string
import numpy as np
import sqlite3
import io

class PCBStep:
    def __init__(self, name, para_array, pcb, pcb_id):
        self.name = name
        self.para_array = para_array
        self.pcb = pcb
        self.pcb_id = pcb_id
        self.rtime = 0

    def doFunc(self):
        if self.pcb_id == 0:
            ret = self.pcb.doFunc(10)
            if type(ret) == int:
                self.rtime = ret

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

class COSQLite:
    def __init__(self, dbname = 'data.db'):
        self.conn = sqlite3.connect('data.db')
        self.cursor = self.conn.cursor()
        return

    def __del__(self):
        self.conn.close()
        return

    def adapt_array(self, arr):
        out = io.BytesIO()
        np.save(out, arr)
        out.seek(0)
        return sqlite3.Binary(out.read())

    def convert_array(self, text):
        out = io.BytesIO(text)
        out.seek(0)
        return np.load(out)

    def queryLogin(self, username, password):
        self.cursor.execute('SELECT * from USERDATA where USERNAME="%s" and PASSWORD="%s"' % (username, password))
        if self.cursor.fetchone():
            return True
        return False

    def queryUser(self, username):
        self.cursor.execute('SELECT * from USERDATA where USERNAME="%s"' % (username))
        if self.cursor.fetchone():
            return True
        return False

    def queryPCRResults(self):
        ret_results = []
        self.cursor.execute('SELECT * from PCRRESULT')

        for ret in self.cursor.fetchall():
            '''
            ret[0] = uid
            ret[1] = testid
            ret[2] = testname
            ret[3] = timestamp
            ret[4] = ct1
            ret[5] = ct2
            ret[6] = w1array
            ret[7] = w2array
            '''
            temp_result = PCRResults(test_id = ret[1], test_name = ret[2], timestamp = ret[3],
	                                 ct1 = ret[4], ct2 = ret[5], well1_array = self.convert_array(ret[6]), well2_array = self.convert_array(ret[7]))

            ret_results.append(temp_result)

        return ret_results

    def addPCRResult(self, pcrresult):
        tid = pcrresult.test_id
        tname = pcrresult.test_name
        ts = pcrresult.timestamp
        ct1 = pcrresult.ct1
        ct2 = pcrresult.ct2
        w1a = self.adapt_array(pcrresult.well1_array)
        w2a = self.adapt_array(pcrresult.well2_array)

        self.cursor.execute("INSERT INTO PCRRESULT (testid, testname, timestamp, ct1, ct2, w1array, w2array) VALUES(?, ?, ?, ?, ?, ?, ?)", 
                            [tid, tname, ts, ct1, ct2, w1a, w2a])

        self.conn.commit()

        return
