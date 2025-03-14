import copcb


def showCmd():
    print("Input command number to do the following task")
    print("    [0] eject cartridge")
    print("    [1] insert cartridge and move to the bottom position")
    print("    [2] move in rocker arm")
    print("    [3] rotate to pos 0")
    print("    [4] rotate to pos 1")
    print("    [5] rotate to pos 2")
    print("    [6] rotate to pos 3")
    print("    [7] rotate to pos 4")
    print("    [8] rotate to pos 5")
    print("    [9] move out rocker arm")
    print("    [10] BLDC clockwise to 1000 RPM")
    print("    [11] BLDC stop")
    print("    [12] BLDC counter clockwise to 1000 RPM")
    print("    [13] BLDC stop")
    print("    [t] Vertical Top")
    print("    [m] Vertical Mid")
    print("    [b] Vertical Btm")
    print("    [o] Cup Driver Move Out 0.05 s")
    print("    [i] Cup Driver Move In 0.05 s")
    print("    [s] QRCode Reader Scan")
    print("    [v] Cartridge Vibration")
    print("    [2-4] Add EtOH, mix")
    print("    [test] test all leds")
    print("==== key in 'done' will exit the program ====")

def showCurState(state):
    if state == -1:
        print("==== Just launching ====")
    else:
        print("==== Last Step is [%d] ====" % state)


def doCmd(pcb, state):
    if state == 0:
        # eject
        pcb.ejectCart()
    elif state == 1:
        ret = pcb.insertCart(timeout=20)
        if ret == True:
            print("Cartridge Inserted")
            # TODO: move to btn
        elif ret == "NO_CARTRIDGE_INSERTED":         # 20240422 TODO
            print("Error: insert cartridge failed, closed directly")
            pcb.forceCloseCart()
        else:
            print("Error: close door error....")
            pcb.forceCloseCart()
    elif state == 2:
        pcb.moveRArm(timeout = 10, release = False)
    elif state == 3:
        pcb.rotateCart(timeout = 10, pos = 0)
    elif state == 4:
        pcb.rotateCart(timeout = 10, pos = 1)
    elif state == 5:
        pcb.rotateCart(timeout = 10, pos = 2)
    elif state == 6:
        pcb.rotateCart(timeout = 10, pos = 3)
    elif state == 7:
        pcb.rotateCart(timeout = 10, pos = 4)
    elif state == 8:
        pcb.rotateCart(timeout = 10, pos = 5)
    elif state == 9:
        pcb.moveRArm(timeout = 10, release = True)
    elif state == 10:
        pcb.startBLDCMotor(rpm = 66, clockwise = True)
        #pcb.setBLDCMotorRPM(timeout = 10, rpm = 66)
    elif state == 11:
        pcb.stopBLDCMotor()
    elif state == 12:
        pcb.startBLDCMotor(rpm = 66, clockwise = False)
        #pcb.setBLDCMotorRPM(timeout = 10, rpm = 66)
    elif state == 13:
        pcb.stopBLDCMotor()

def testLEDs(pcb):
    # 2-4.4 turn on L-pump
    pcb.turnOnVacAirPump(timeout = 5)
    # 2-4.6 turn on V-pump
    pcb.turnOnRVacAirPump(timeout = 5)
    # 2-4.7 open valve 4
    pcb.setVacAirPump(timeout = 5, number = 1, time = 3000)
    pcb.setVacAirPump(timeout = 5, number = 2, time = 3000)
    pcb.setVacAirPump(timeout = 5, number = 3, time = 3000)
    pcb.setVacAirPump(timeout = 5, number = 4, time = 3000)
    pcb.setVacAirPump(timeout = 5, number = 5, time = 3000)
    pcb.setVacAirPump(timeout = 5, number = 6, time = 3000)
    pcb.setVacAirPump(timeout = 5, number = 7, time = 3000)
    pcb.setVacAirPump(timeout = 5, number = 8, time = 3000)
    pcb.turnOffVacAirPump(timeout = 5)
    pcb.turnOffRVacAirPump(timeout = 5)
    return

def testLEDs2(pcb):
    # 2-4.4 turn on L-pump
    pcb.turnOnVacAirPump(timeout = 5)
    return


# 2-4, Add EtOH, mix
def etoh(pcb):
    # 2-4.1, rocker arm move in
    pcb.moveRArm(timeout = 10, release = False)
    # 2-4.2 rotate to postion 0
    pcb.rotateCart(timeout = 10, pos = 0)
    # 2-4.3 move to middle position
    pcb.moveVertPosMid()
    # 2-4.4 turn on L-pump
    pcb.turnOnVacAirPump(timeout = 5)
    # 2-4.5 rocker arm move out
    pcb.moveRArm(timeout = 10, release = True)
    # 2-4.6 turn on V-pump
    pcb.turnOnRVacAirPump(timeout = 5)
    # 2-4.7 open valve 4
    pcb.setVacAirPump(timeout = 5, number = 4, time = 100)
    # 2-4.8 open valve 7
    pcb.setVacAirPump(timeout = 5, number = 7, time = 100)
    # 2-4.9 pull S.pump
    # 2-4.10 close valve 4
    pcb.setVacAirPump(timeout = 5, number = 4, time = 0)
    # 2-4.11 close valve 7
    pcb.setVacAirPump(timeout = 5, number = 7, time = 0)
    # 2-4.12 turn off V-pump
    pcb.turnOffRVacAirPump(timeout = 5)
    # 2-4.13 turn off L-pump
    pcb.turnOffVacAirPump(timeout = 5)
    # 2-4.14 open S.valve
    # 2-4.15 push S.pump
    # 2-4.16 close S.valve
    # 2-4.17 move to bottom position
    pcb.moveVertPosBtm()
    return

# 2-5, Incubate, 4'C 10min
def incubate(pcb):
    # 2-5.1 rocker arm move in
    pcb.moveRArm(timeout = 10, release = False)
    # 2-5.2 rotate to position 1
    pcb.rotateCart(timeout = 10, pos = 1)
    # 2-5.3 move to middle position
    pcb.moveVertPosMid()
    # 2-5.4 turn on L-pump
    pcb.turnOnVacAirPump(timeout = 5)
    # 2-5.5 rocker arm move out
    pcb.moveRArm(timeout = 10, release = True)
    # 2-5.6 move tec up (optical module)
    pcb.moveOPos(timeout = 5, up = True)
    # 2-5.7 tec on
    pcb.turnOnTEC(timeout = 5, pwm = 5)
    # 2-5.8 tec off
    pcb.turnOffTEC(timeout = 5)
    # 2-5.9 move tec down
    pcb.moveOPos(timeout = 5, up = False)
    # 2-5.10 turn off L-pump
    pcb.turnOffVacAirPump(timeout = 5)
    # 2-5.11 move to buttom position
    pcb.moveVertPosBtm()
    return

# 2-6, centrifuge through filter 1
def centrifuge1(pcb):
    # 2-6.1 turn on BLDC clockwise 1000 rpm
    pcb.startBLDCMotor(rpm = 1000, clockwise = True)
    # 2-6.2 rocker arm move in
    pcb.moveRArm(timeout = 10, release = False)
    # 2-6.3 rotate to pos 0
    pcb.rotateCart(timeout = 10, pos = 0)
    # 2-6.4 move to middle position
    pcb.moveVertPosMid()
    # 2-6.5 turn on L-pump
    pcb.turnOnVacAirPump(timeout = 5)
    # 2-6.6 rocker arm move out
    pcb.moveRArm(timeout = 10, release = True)
    # 2-6.7 Turn on V-pump
    pcb.turnOnRVacAirPump(timeout = 5)
    # 2-6.8 Open valve 1
    pcb.setVacAirPump(timeout = 5, number = 1, time = 100)
    # 2-6.9 Open valve 8
    pcb.setVacAirPump(timeout = 5, number = 8, time = 100)
    # 2-6.10 Pull S.pump
    # 2-6.11 Close valve 1
    pcb.setVacAirPump(timeout = 5, number = 1, time = 0)
    # 2-6.12 Close valve 8
    pcb.setVacAirPump(timeout = 5, number = 8, time = 0)
    # 2-6.13 Turn off V-pump
    pcb.turnOffRVacAirPump(timeout = 5)
    # 2-6.14 Open S.valve
    # 2-6.15 Push S.pump
    # 2-6.16 Close S.valve
    return

# 2-7, add wash buffer 1
def buffer1(pcb):
    # 2-7.1 turn on V-pump
    pcb.turnOnRVacAirPump(timeout = 5)
    # 2-7.2 open valve 2
    pcb.setVacAirPump(timeout = 5, number = 2, time = 100)
    # 2-7.3 open valve 7
    pcb.setVacAirPump(timeout = 5, number = 7, time = 100)
    # 2-7.4 pull s.pump
    # 2-7.5 close valve 2
    pcb.setVacAirPump(timeout = 5, number = 2, time = 0)
    # 2-7.6 close valve 7
    pcb.setVacAirPump(timeout = 5, number = 7, time = 0)
    # 2-7.7 turn off V-pump
    pcb.turnOffRVacAirPump(timeout = 5)
    # 2-7.8 turn off L-pump
    pcb.turnOffVacAirPump(timeout = 5)
    # 2-7.9 open S.valve
    # 2-7.10 push S.pump
    # 2-7.11 close S.valve
    # 2-7.12 move to buttom position
    pcb.moveVertPosBtm()
    return
    
# 2-8, centrifuge through filter 1
def filter1(pcb):
    # 2-8.1 turn on bldc clockwise, 1000rpm
    pcb.startBLDCMotor(rpm = 1000, clockwise = True)
    # 2-8.2 rocker arm move in
    pcb.moveRArm(timeout = 10, release = False)
    # 2-8.3 rotate to pos 0
    pcb.rotateCart(timeout = 10, pos = 0)
    # 2-8.4 move to middle position
    pcb.moveVertPosMid()
    # 2-8.5 turn on L-pump
    pcb.turnOnVacAirPump(timeout = 5)
    # 2-8.6 rocker arm move out
    pcb.moveRArm(timeout = 10, release = True)
    # 2-8.7 turn on V-pump
    pcb.turnOnRVacAirPump(timeout = 5)
    # 2-8.8 open valve 1
    pcb.setVacAirPump(timeout = 5, number = 1, time = 100)
    # 2-8.9 open valve 8
    pcb.setVacAirPump(timeout = 5, number = 8, time = 100)
    # 2-8.10 pull S.pump
    # 2-8.11 close valve 1
    pcb.setVacAirPump(timeout = 5, number = 1, time = 0)
    # 2-8.12 close valve 8
    pcb.setVacAirPump(timeout = 5, number = 8, time = 0)
    # 2-8.13 turn off v-pump
    pcb.turnOffRVacAirPump(timeout = 5)
    # 2-8.14 open S.valve
    # 2-8.15 push S.pump
    # 2-8.16 close S.valve
    return

# 2-9, add wash buffer 2
def buffer2(pcb):
    # 2-9.1 Turn on V-pump
    pcb.turnOnRVacAirPump(timeout = 5)
    # 2-9.2 Open valve 6
    pcb.setVacAirPump(timeout = 5, number = 6, time = 100)
    # 2-9.3 Open valve 7
    pcb.setVacAirPump(timeout = 5, number = 7, time = 100)
    # 2-9.4 Pull S.pump
    # 2-9.5 Close valve 6
    pcb.setVacAirPump(timeout = 5, number = 6, time = 0)
    # 2-9.6 Close valve 7
    pcb.setVacAirPump(timeout = 5, number = 7, time = 0)
    # 2-9.7 Turn off V-pump
    pcb.turnOffRVacAirPump(timeout = 5)
    # 2-9.8 Turn off L-pump
    pcb.turnOffVacAirPump(timeout = 5)
    # 2-9.9 Open S.valve
    # 2-9.10 Push S.pump
    # 2-9.11 Close S.valve
    # 2-9.12 Move to bottom position
    pcb.moveVertPosBtm()
    return

# 2-10, centrifuge through filter 2, 6000g, 30s
# same as 2-8

# 3-1 heat elution buffer, 40C 2min
def heat_elu_buffer(pcb):
    # 3-1.1 Rocker arm move in
    pcb.moveRArm(timeout = 10, release = False)
    # 3-1.2 Rotate to position 1
    pcb.rotateCart(timeout = 10, pos = 1)
    # 3-1.3 Move to middle position
    pcb.moveVertPosMid()
    # 3-1.4 Turn on L-pump
    pcb.turnOnVacAirPump(timeout = 5)
    # 3-1.5 Rocker arm move out
    pcb.moveRArm(timeout = 10, release = True)
    # 3-1.6 Move TEC up
    pcb.moveOPos(timeout = 5, up = True)
    # 3-1.7 TEC on with regulation
    pcb.turnOnTEC(timeout = 5, pwm = 5)
    # 3-1.8 TEC off
    pcb.turnOffTEC(timeout = 5)
    # 3-1.9 Move TEC down
    pcb.moveOPos(timeout = 5, up = False)
    # 3-1.10 Turn off L-pump
    pcb.turnOffVacAirPump(timeout = 5)
    # 3-1.11 Move to bottom position
    pcb.moveVertPosBtm()
    return

# 3-2 add elution buffer, 60uL
def add_elu_buffer(pcb):
    # 3-2.1 Rocker arm move in
    pcb.moveRArm(timeout = 10, release = False)
    # 3-2.2 Rotate to position 0
    pcb.rotateCart(timeout = 10, pos = 0)
    # 3-2.3 Move to middle position
    pcb.moveVertPosMid()
    # 3-2.4 Turn on L-pump
    pcb.turnOnVacAirPump(timeout = 5)
    # 3-2.5 Rocker arm move out
    pcb.moveRArm(timeout = 10, release = True)
    # 3-2.6 Turn on V-pump
    pcb.turnOnRVacAirPump(timeout = 5)
    # 3-2.7 Open valve 5
    pcb.setVacAirPump(timeout = 5, number = 5, time = 100)
    # 3-2.8 Open valve 7
    pcb.setVacAirPump(timeout = 5, number = 7, time = 100)
    # 3-2.9 Pull S.pump
    # 3-2.10 Close valve 5
    pcb.setVacAirPump(timeout = 5, number = 5, time = 0)
    # 3-2.11 Close valve 7
    pcb.setVacAirPump(timeout = 5, number = 7, time = 0)
    # 3-2.12 Turn off V-pump
    pcb.turnOffRVacAirPump(timeout = 5)
    # 3-2.13 Turn off L-pump
    pcb.turnOffVacAirPump(timeout = 5)
    # 3-2.14 Open S.valve
    # 3-2.15 Push S.pump
    # 3-2.16 Close S.valve
    # 3-2.17 Move to bottom position
    pcb.moveVertPosBtm()
    return
    
# 3-3 centrifuge through filter 1
# same as 2-8

# initial pcb
btpcb = copcb.ModuleBT()
btpcb.initPCB()

# inital qrcr0
#qrcr = copcb.QRCodeReader()
#qrcr.initPCB()

# initial qrcodereader

cur_state = -1

# show command log


# Initializing an empty list to store numbers
number_list = []
 
# Prompting the user to enter numbers
while True:
    showCmd()
    showCurState(cur_state)
    num = input("input> ")
    if num == 'done':
        break
    elif num == 't':
        btpcb.moveVertPosTop()
    elif num == 'm':
        btpcb.moveVertPosMid()
    elif num == 'b':
        btpcb.moveVertPosBtm()
    elif num == 'o':
        btpcb.moveCDriver(timeout = 0.05, back = False)
    elif num == 'i':
        btpcb.moveCDriver(timeout = 0.05, back = True)
    elif num == 's':
        #ret = qrcr.scan()
        print("==== QRCodeReader Scan Result = %s" % ret)
    elif num == 'v':
        btpcb.vibrateCart(totaltime = 60)
    elif num == '2-4':
        etoh(btpcb)
    elif num == 'test':
        testLEDs(btpcb)
    elif num == 'test2':
        testLEDs2(btpcb)

    elif num == '':
        cur_state += 1
        if cur_state >= 14:
            cur_state -= 14
        doCmd(btpcb, cur_state)
    else:
        cur_state = int(num)
        doCmd(btpcb, cur_state)

    #number_list.append(cur_state)
 
# Printing the list of numbers
#print("List of numbers:", number_list)




