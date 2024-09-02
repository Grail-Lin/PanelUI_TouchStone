import copcb


def showCmd():
    print("Input command number to do the following task")
    print("    [0] eject cartridge")
    print("    [1] insert cartridge and move to the bottom position")
    print("    [2] move in rocker arm")
    print("    [3] rotate to pos 0")
    print("    [4] rotate to pos 60")
    print("    [5] rotate to pos 90")
    print("    [6] rotate to pos 120")
    print("    [7] rotate to pos 180")
    print("    [8] rotate to pos 300")
    print("    [9] move out rocker arm")
    print("    [10] BLDC clockwise to 1000 RPM")
    print("    [11] BLDC stop")
    print("    [12] BLDC counter clockwise to 1000 RPM")
    print("    [13] BLDC stop")
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
        else:
            print("Error: close door error....")
    elif state == 2:
        pcb.moveRArm(timeout = 10, release = False)
    elif state == 3:
        pcb.rotateCart(timeout = 10, pos = 0)
    elif state == 4:
        pcb.rotateCart(timeout = 10, pos = 60)
    elif state == 5:
        pcb.rotateCart(timeout = 10, pos = 90)
    elif state == 6:
        pcb.rotateCart(timeout = 10, pos = 120)
    elif state == 7:
        pcb.rotateCart(timeout = 10, pos = 180)
    elif state == 8:
        pcb.rotateCart(timeout = 10, pos = 300)
    elif state == 9:
        pcb.moveRArm(timeout = 10, release = True)
    elif state == 10:
        pcb.setBLDCMotorRPM(timeout = 10, rpm = 1000)
        pcb.startBLDCMotor(timeout = 5, clockwise = True)
    elif state == 11:
        pcb.stopBLDCMotor()
    elif state == 12:
        pcb.setBLDCMotorRPM(timeout = 10, rpm = 1000)
        pcb.startBLDCMotor(timeout = 5, clockwise = False)
    elif state == 13:
        pcb.stopBLDCMotor()


# initial pcb
btpcb = copcb.ModuleMock()
btpcb.initPCB()

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
    elif num == '':
        cur_state += 1
        if cur_state >= 14:
            cur_state -= 14
    else:
        cur_state = int(num)

    doCmd(btpcb, cur_state)
    #number_list.append(cur_state)
 
# Printing the list of numbers
#print("List of numbers:", number_list)




