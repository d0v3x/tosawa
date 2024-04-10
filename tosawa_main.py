import serial
import time
import subprocess
import datetime
import requests

ser = serial.Serial('/dev/ttyUSB0', 115200)
previousSensorState = b'0'
file_path = "/home/pi/ai101/oneshot.py"
line_notify_token = 'SgLJdERR1UILnOnXoeXGX7AG7Gd2EBN1eFVeEyrSYGs'

while True:
    sensorState = ser.readline().strip()  
    if sensorState != previousSensorState:
        if sensorState == b'1':  
            print("磁気センサーが離れました。")
            time.sleep(1)
            subprocess.call(['python', file_path]) 

            if time.sleep(60):
                message = f"一時間が経過しました。055-xxx-xxxx に電話してください。"
                now = datetime.datetime.now()
                timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
                message_with_timestamp = f"{message} (現在の時間: {timestamp})"

                def send_line_notify_with_message(notification_message):
                    headers = {
                        'Authorization': f'Bearer {line_notify_token}'
                    }
                    payload = {
                        'message': notification_message,
                    }
                    requests.post('https://notify-api.line.me/api/notify', headers=headers, data=payload)

                send_line_notify_with_message(message_with_timestamp)
                print("LINEの送信が完了しました。")
            else:
                print("磁気センサーが近づきました。")
            previousSensorState = sensorState

ser.close()

