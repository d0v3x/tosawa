import serial
import time
import subprocess

ser = serial.Serial('/dev/ttyUSB0', 115200)
previousSensorState = b'0'
file_path = "/home/pi/ai101/oneshot.py"

while True:
    sensorState = ser.readline().strip()  
    if sensorState != previousSensorState:
        if sensorState == b'1':  
            print("磁気センサーが離れました。")
            time.sleep(1)
            subprocess.call(['python',file_path]) 
        else:
            print("磁気センサーが近づきました。")
        previousSensorState = sensorState
ser.close()
