import serial
import time

# 設定 Arduino 連接埠 (請修改為你的 Arduino COM Port)
arduino = serial.Serial(port="COM3", baudrate=9600, timeout=1)
time.sleep(2)  # 等待 Arduino 初始化

def send_command(command):
    """ 發送指令給 Arduino """
    arduino.write(command.encode())  # 發送指令
    time.sleep(0.5)  # 等待執行

def get_rotation():
    """ 取得 Arduino 回傳的旋轉圈數 """
    arduino.write(b'S')  # 送出停止指令
    time.sleep(0.5)  # 等待 Arduino 回應
    data = arduino.readline().decode().strip()  # 讀取 Arduino 回傳資料
    return float(data) if data else 0.0  # 解析回傳數值

# 測試



#send_command("F")  # 順時針轉
#time.sleep(1)

#send_command("B")  # 逆時針轉
#time.sleep(1)

#rotation_count = get_rotation()  # 取得目前旋轉的圈數
#print(f"目前旋轉了 {rotation_count} 圈")



def showCmd():
    print("Input command number to do the following task")
    print("    [F] clockwise")
    print("    [B] anti-clockwise")
    print("    [S] stop and print steps")
    print("==== key in 'done' will exit the program ====")




# Prompting the user to enter numbers
while True:
    showCmd()
    num = input("input> ")
    if num == 'done':
        break
    elif num == 'F':
        send_command("F")
        time.sleep(1)
    elif num == 'B':
        send_command("B")
        time.sleep(1)
    elif num == 'S':
        rotation_count = get_rotation()
        print("目前旋轉了 %f 圈" % rotation_count)