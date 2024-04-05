import serial
import time
import subprocess

ser = serial.Serial('/dev/ttyUSB0', 115200)
previousSensorState = b'0'

while True:
    sensorState = ser.readline().strip()  
    if sensorState != previousSensorState:
        if sensorState == b'1':  
            print("磁気センサーが離れました。")
            subprocess.run(['raspistill', '-o', 'Pictures/image.jpg']) 
        else:
            print("磁気センサーが近づきました。")
        previousSensorState = sensorState
ser.close()
