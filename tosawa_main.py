import serial
import time
import subprocess
import datetime
import requests

# ESP32側とのシリアル通信の設定
ser = serial.Serial('/dev/ttyUSB0', 115200)

# 磁気センサーの状態をバイト文字として保持する関数
previousSensorState = b'0'

# 撮影プログラムのパスを定義
file_path = "/home/pi/ai101/oneshot.py"

# 磁気センサーの変化をトリガーに感知するメインの関数
while True:
    # ESP32から磁気センサーの値を読み続ける
    sensorState = ser.readline().strip()
    
    # 現在の磁気センサーの値と保持している値が異なる場合
    if sensorState != previousSensorState:
        if sensorState == b'1':  
            print("磁気センサーが離れました。")
            
            # 磁気センサーが離れた時に撮影プログラムを動かす
            subprocess.call(['python', file_path]) 
        else:
            print("磁気センサーが近づきました。")
        # 磁気センサーの状態を保存
        previousSensorState = sensorState

ser.close()


