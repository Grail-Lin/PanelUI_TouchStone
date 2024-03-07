import random, time, string
import numpy as np
import sqlite3
import io

class PCBStep:
    def __init__(self, name, counter, para_array, pcb, pcb_id, run_time=1, repeat=1):


        self.name = name
        self.pcb = pcb
        self.pcb_id = pcb_id
        self.rtime = run_time  #pcb.total_time

        #self.pcb_list = pcb_list
        self.para_array = para_array

        self.repeat = repeat
		
		

    def doFunc(self):
        # use pcb_id to do target method
        if self.pcb_id == 0:
            ret = self.pcb.doFunc(10)
            if type(ret) == int:
                self.rtime = ret
        # 101: rorateCart
        elif self.pcb_id == 101:
            ret = self.pcb.rotateCart(self.para_array[0], self.para_array[1])
        # 401: moveOPos
        elif self.pcb_id == 401:
		    ret = self.pcb.moveOPos(self.para_array[0], self.para_array[1])
        # 801: moveVertPosTop
        elif self.pcb_id == 801:
		    ret = self.pcb.moveVertPosTop(self.para_array[0])
        # 802: moveVertPosMid
        elif self.pcb_id == 802:
		    ret = self.pcb.moveVertPosMid(self.para_array[0])
        # 803: moveVertPosBtm
        elif self.pcb_id == 803:
		    ret = self.pcb.moveVertPosBtm(self.para_array[0])
        # 901: startBLDCMotor
        elif self.pcb_id == 901:
		    ret = self.pcb.startBLDCMotor(self.para_array[0], self.para_array[1])
        # 902: stopBLDCMotor
        elif self.pcb_id == 902:
		    ret = self.pcb.stopBLDCMotor(self.para_array[0])
        # 903: setBLDCMotorRPM
        elif self.pcb_id == 903:
		    ret = self.pcb.setBLDCMotorRPM(self.para_array[0], self.para_array[1])
            # need to wait for count time?
        # 1001: turnOnVacAirPump
        elif self.pcb_id == 1001:
		    ret = self.pcb.turnOnVacAirPump(self.para_array[0])
        # 1002: turnOffVacAirPump
        elif self.pcb_id == 1002:
		    ret = self.pcb.turnOffVacAirPump(self.para_array[0])
        # 1003: setVacAirPump
        elif self.pcb_id == 1003:
		    ret = self.pcb.setVacAirPump(self.para_array[0], self.para_array[1], self.para_array[2])
		# 1402: turnOffTEC
        elif self.pcb_id == 1402:
		    ret = self.pcb.turnOffTEC(self.para_array[0])
		# 1503: turnOnWaterPump
        elif self.pcb_id == 1503:
		    ret = self.pcb.turnOnWaterPump(self.para_array[0])
		# 1504: turnOffWaterPump
        elif self.pcb_id == 1504:
		    ret = self.pcb.turnOffWaterPump(self.para_array[0])
        # 2004: controlBothHeater
        elif self.pcb_id == 2004:
		    ret = self.pcb.controlBothHeater(self.para_array[0], self.para_array[1], self.para_array[2])
        # 2005: controlPIDBothHeater
        elif self.pcb_id == 2005:
		    ret = self.pcb.controlPIDBothHeater(self.para_array[0], self.para_array[1], self.para_array[2], self.para_array[3])
		# 2006: controlPIDTEC
        elif self.pcb_id == 2006:
		    ret = self.pcb.controlPIDTEC(self.para_array[0], self.para_array[1], self.para_array[2], self.para_array[3])

        return ret


class PCBsStep:
    # name = step name
    # pcb_list = [PCB, PCB, PCB....]
    # pcd_id_list = id to identify the pcb
    # para_list = para for pcb
    # time_list = time for pcb each
    # repeat = repeat times
    def __init__(self, name, pcb_list, pcb_id_list, para_list, time_list, repeat=1):
        self.name = name

        self.pcb_list = pcb_list
        self.pcb_id_list = pcb_id_list
        self.para_list = para_list

        self.repeat = repeat
		
		
        self.cur_pcb_num = 0
        self.cur_repeat_num = 0


        self.rtime = 0
        for tt in time_list:
           self.rtime += tt



    def doFunc(self, current_time):
        # check current pcb
        temp_time = 0

        for jj in range(0, self.repeat):
            for ii in range(0, len(time_list)):
                temp_time += time_list[ii]
                if current_time <= temp_time:
                    self.cur_pcb_num = ii
                    self.cur_repeat_num = jj
                    break
            else:
                continue
            break

        if pcb_id_list[self.cur_pcb_num] == 0:
            ret = self.pcb.doFunc(10)

class UserData:
    def __init__(self, username = None, password = None, timestamp = None, role = 3):
        self.username = username
        self.password = password
        self.timestamp = timestamp
        self.role = role
        return

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

    def updatePasswd(self, username, password):
        try:
            self.cursor.execute('UPDATE USERDATA SET PASSWORD="%s" WHERE USERNAME="%s"' % (password, username))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def queryUserLists(self):
        ret_users = []
        self.cursor.execute('SELECT * from USERDATA')

        for ret in self.cursor.fetchall():
            '''
            ret[0] = uid
            ret[1] = username
            ret[2] = password
            ret[3] = timestamp
            ret[4] = role (0 = not use, 1 = admin, 2 = advance, 3 = normal)
            '''
            temp_user = UserData(username = ret[1], password = ret[2], timestamp = ret[3], role = ret[4])

            ret_users.append(temp_user)

        return ret_users

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
