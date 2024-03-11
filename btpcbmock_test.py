
import time


# PCB module
import copcb
import coutil
import random




if __name__ == "__main__":

    # init moduleBT
    print("==== Init the BT PCB ====")
    print("target desc: USB Serial Port")
    btpcb = copcb.ModuleBTMock()
    btpcb.initPCB()
    

    # 20 combo cmd:
    # test: open door + eject cart
    print("TEST #0-1 open door + eject cart, combo cmd: 20,1,60000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.ejectCart()
        print("Result: " + str(ret))
        input("Press any key to do next test")
    
    # test: insert cart + close door
    print("TEST #0-2 insert cart + close door, combo cmd: 20,2,60000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.insertCart()
        print("Result: " + str(ret))
        input("Press any key to do next test")
    
    # 3: rocker arm
    print("TEST #3-2 lock rocker arm, 3 cmd: 3,2,2000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.moveRArm(release = False)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    # 7: move cartridge roller
    print("TEST #7-1 move Carttridge Roller forward, 7 cmd: 7,2,6000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.moveCartRoller(back = False)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #7-2 move Carttridge Roller backward, 7 cmd: 7,1,6000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.moveCartRoller(back = True)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    # 1: cartridge rotation
    print("TEST #1-1 rotate cartridge to pos = 0, 1 cmd: 1,1,10000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.rotateCart()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #1-2 rotate cartridge to pos = 90, 1 cmd: 1,2,90,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.rotateCart(pos=90)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #1-3 rotate cartridge to pos = 150, 1 cmd: 1,2,150,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.rotateCart(pos=150)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    # 3: rocker arm
    print("TEST #3-1 release rocker arm, 3 cmd: 3,1,2000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.moveRArm(release = True)
        print("Result: " + str(ret))
        input("Press any key to do next test")


    # 6: door
    print("TEST #6-1 open door, 6 cmd: 6,1,1000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.openDoor()
        print("Result: " + str(ret))
        input("Press any key to do next test")


    # 2: cup driver
    print("TEST #2-1 move Cup Driver forward, 2 cmd: 2,2,3000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.moveCDriver(back = False)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #2-2 move Cup Driver backward, 2 cmd: 2,1,3000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.moveCDriver(back = True)
        print("Result: " + str(ret))
        input("Press any key to do next test")


    print("TEST #6-2 close door, 6 cmd: 6,2,1000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.closeDoor()
        print("Result: " + str(ret))
        input("Press any key to do next test")





    # 4: optical position
    print("TEST #4-1 move optical position up, 4 cmd: 4,1,2000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.moveOPos(up = True)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #4-2 move optical position down, 4 cmd: 4,2,2000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.moveOPos(up = False)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    # 5: reverses motor
    print("NOTYET, TEST #5 reverse motor for move optical position, 5 cmd:")
    input("Press any key to next test")



    # 8: vertical position
    print("TEST #8-1 move vertical position to Btm, 8 cmd: 8,3,36000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.moveVertPosBtm()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #8-2 move vertical position to Top, 8 cmd: 8,1,36000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.moveVertPosTop()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #8-3 move vertical position to Mid, 8 cmd: 8,2,18000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.moveVertPosMid()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    # 9: BLDC Motor
    print("TEST #9-1 start BLDC Motor (CW), 9 cmd: 9,1,5000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.startBLDCMotor(clockwise = True)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #9-2 set BLDC Motor 5000 RPM (CW), 9 cmd: 9,5,5000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.setBLDCMotorRPM(rpm = 5000)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #9-3 set BLDC Motor 3000 RPM (CW), 9 cmd: 9,5,3000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.setBLDCMotorRPM(rpm = 3000)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #9-4 stop BLDC Motor , 9 cmd: 9,3,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.stopBLDCMotor()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #9-5 start BLDC Motor (CCW), 9 cmd: 9,2,5000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.startBLDCMotor(clockwise = False)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #9-6 set BLDC Motor 5000 RPM (CCW), 9 cmd: 9,5,5000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.setBLDCMotorRPM(rpm = 5000)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #9-7 set BLDC Motor 10000 RPM (CCW), 9 cmd: 9,5,10000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.setBLDCMotorRPM(rpm = 10000)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #9-8 stop BLDC Motor , 9 cmd: 9,3,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.stopBLDCMotor()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    # 10: vacuum air pump
    print("TEST #10-1 turn on vacuum air pump, 10 cmd: 10,1,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOnVacAirPump()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #10-2 set vacuum air pump 1 for 1000ms, 10 cmd: 10,3,1000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.setVacAirPump(timeout = 5, number = 1, time = 1000)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #10-3 turn off vacuum air pump, 10 cmd: 10,2,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOffVacAirPump()
        print("Result: " + str(ret))
        input("Press any key to do next test")


    print("TEST #10-4 turn on vacuum air pump, 10 cmd: 10,1,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOnVacAirPump()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #10-5 set vacuum air pump 2 for 2000ms, 10 cmd: 10,4,2000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.setVacAirPump(timeout = 5, number = 2, time = 2000)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #10-6 turn off vacuum air pump, 10 cmd: 10,2,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOffVacAirPump()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #10-7 turn on vacuum air pump, 10 cmd: 10,1,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOnVacAirPump()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #10-8 set vacuum air pump 3 for 3000ms, 10 cmd: 10,5,3000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.setVacAirPump(timeout = 5, number = 3, time = 3000)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #10-9 turn off vacuum air pump, 10 cmd: 10,2,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOffVacAirPump()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #10-10 turn on vacuum air pump, 10 cmd: 10,1,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOnVacAirPump()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #10-11 set vacuum air pump 4 for 1000ms, 10 cmd: 10,6,1000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.setVacAirPump(timeout = 5, number = 4, time = 1000)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #10-12 turn off vacuum air pump, 10 cmd: 10,2,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOffVacAirPump()
        print("Result: " + str(ret))
        input("Press any key to do next test")


    print("TEST #10-13 turn on vacuum air pump, 10 cmd: 10,1,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOnVacAirPump()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #10-14 set vacuum air pump 5 for 2000ms, 10 cmd: 10,7,2000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.setVacAirPump(timeout = 5, number = 5, time = 2000)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #10-15 turn off vacuum air pump, 10 cmd: 10,2,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOffVacAirPump()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #10-16 turn on vacuum air pump, 10 cmd: 10,1,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOnVacAirPump()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #10-17 set vacuum air pump 6 for 3000ms, 10 cmd: 10,8,3000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.setVacAirPump(timeout = 5, number = 6, time = 3000)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #10-18 turn off vacuum air pump, 10 cmd: 10,2,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOffVacAirPump()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    # 11: reserves air pump
    print("TEST #11-1 turn on reserves vacuum air pump, 11 cmd: 11,1,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOnRVacAirPump()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #11-2 set reserves vacuum air pump 1 for 1000ms, 11 cmd: 11,3,1000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.setRVacAirPump(timeout = 5, number = 1, time = 1000)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #11-3 set reserves vacuum air pump 2 for 2000ms, 11 cmd: 11,4,2000,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.setRVacAirPump(timeout = 5, number = 2, time = 2000)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #11-4 turn off vacuum air pump, 11 cmd: 11,2,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOffRVacAirPump()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    # 12: heater
    print("TEST #12-1 turn on heater for 95 degree, 12 cmd: 12,1,5,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        pwm_value = 5
        if keyin != "":
            pwm_value = int(keyin)
        ret = btpcb.turnOnHeater(pwm = pwm_value)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #12-2 measure heater, 12 cmd: 12,4,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.measureHeater()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #12-3 measure heater, 12 cmd: 12,4,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.measureHeater()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #12-4 turn off heater, 12 cmd: 12,2,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOffHeater()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    # 13: reserves heater
    print("TEST #13-1 turn on reserves heater, 13 cmd: 13,1,5,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        pwm_value = 5
        if keyin != "":
            pwm_value = int(keyin)
        ret = btpcb.turnOnRHeater(pwm = pwm_value)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #13-2 measure reserves heater, 13 cmd: 13,4,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.measureRHeater()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #13-3 measure reserves heater, 13 cmd: 13,4,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.measureRHeater()
        print("Result: " + str(ret))
        input("Press any key to do next test")


    print("TEST #13-4 turn off reserves heater, 13 cmd: 13,2,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOffRHeater()
        print("Result: " + str(ret))
        input("Press any key to do next test")


    # 15: Water Cooler Fan
    print("TEST #15-1 open water cooler fan, 15 cmd: 15,1,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOnWaterFan()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #15-3 open water cooler pump, 15 cmd: 15,3,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOnWaterPump()
        print("Result: " + str(ret))
        input("Press any key to do next test")


    # 14: TEC
    print("TEST #14-1 turn on TEC, 14 cmd: 14,1,5,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        pwm_value = 5
        if keyin != "":
            pwm_value = int(keyin)
        ret = btpcb.turnOnTEC(pwm = pwm_value)
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #14-2 measure TEC cold, 13 cmd: 14,4,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.measureTECcold()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #14-3 measure TEC hot, 14 cmd: 14,5,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.measureTEChot()
        print("Result: " + str(ret))
        input("Press any key to do next test")


    print("TEST #14-4 turn off TEC, 14 cmd: 14,2,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOffTEC()
        print("Result: " + str(ret))
        input("Press any key to do next test")


    print("TEST #15-2 close water cooler fan, 15 cmd: 15,2,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOffWaterFan()
        print("Result: " + str(ret))
        input("Press any key to do next test")


    print("TEST #15-4 close water cooler pump, 15 cmd: 15,4,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOffWaterPump()
        print("Result: " + str(ret))
        input("Press any key to do next test")


    # 16: system dissipation fan
    print("TEST #16-1 open system dissipation fan, 16 cmd: 16,1,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOnSDFan()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #16-2 close system dissipation fan, 16 cmd: 16,2,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOffSDFan()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    # 17: optical dissipation fan
    print("TEST #17-1 open optical dissipation fan, 17 cmd: 17,1,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOnODFan()
        print("Result: " + str(ret))
        input("Press any key to do next test")

    print("TEST #17-2 close optical dissipation fan, 17 cmd: 17,2,0,0")
    keyin = input("Press any key to start test; 0 to skip test")
    if keyin != "0":
        ret = btpcb.turnOffODFan()
        print("Result: " + str(ret))
        input("Press any key to do next test")




