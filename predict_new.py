import numpy as np
import subprocess
import psutil
from tensorflow.keras.models import load_model
from PIL import Image
import sys
import datetime
import requests

# 外出プログラムの検出メソッドの定義
def check_process(process_name):
    ps_aux_output = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
    for line in ps_aux_output.stdout.split('\n'):
        if process_name in line and 'grep' not in line:
            return True
    return False
    
# 外出プログラムを停止するメソッド
def stop_process(process_name):
    subprocess.run(['pkill', '-f', process_name])

# 外出プログラムを起動するメソッド
def start_process(process_name):
    subprocess.Popen(["python", file_path])

# 監視するプログラム名
program_name = "send_wada.py"

# 外出用プログラムのファイルパス
file_path = "/home/pi/ai101/send_wada.py"

# 識別クラス名と日本語名
class_names = {
    "wada": "和田",
    "sano": "佐野",
    "tomioka": "冨岡"
}

# vgg16用のリサイズ数値の定義
image_size = 224

# 画像を読み込み配列に落とし込む
image_path = sys.argv[1]
image = Image.open(image_path)
image = image.convert("RGB")
image = image.resize((image_size, image_size))
data = np.asarray(image) / 255.0
X = []
X.append(data)
X = np.array(X)

# モデルを読み込む
model = load_model('./tosawa_face_v6.h5')

# 予測を行い、確率とクラス名と日本語名をpercentageとpredicted_class_jpに代入
result = model.predict([X])[0]
predicted_class_index = result.argmax()
percentage = int(result[predicted_class_index] * 100)
predicted_class = list(class_names.keys())[predicted_class_index]
predicted_class_jp = class_names[predicted_class]

# LINE Notifyのアクセストークンを設定
line_notify_token = 'Your token'

# 予測されたクラスが "wada" の場合にメッセージを送信
if predicted_class == "wada":
    # 予測した人物をターミナルに確信度とクラス名を表示
    print(f"予測された人物は {predicted_class_jp} さんで、確信度は {percentage}% です。")
    # 送信するメッセージを作成
    message = f"予測された人物は {predicted_class_jp} さんで、確信度は {percentage}% です。"
    # タイムスタンプを追加
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    message_with_timestamp = f"{message} (撮影日時: {timestamp})"

    # LINE Notifyでメッセージを送信する関数を定義
    def send_line_notify_with_message(notification_message):
        headers = {
            'Authorization': f'Bearer {line_notify_token}'
        }
        payload = {
            'message': notification_message,
        }
        files = {'imageFile': open(image_path, 'rb')}
        requests.post('https://notify-api.line.me/api/notify', headers=headers, data=payload, files=files)

    # LINE Notifyでメッセージを送信
    send_line_notify_with_message(message_with_timestamp)
    print("LINEの送信が完了しました。")
    # 和田さんが外出しているプログラムが動いているかの真偽をチェック。稼働中なら終了し、稼働してないなら起動。
    if check_process(program_name):
         print("和田さんが帰宅しました。")
         stop_process(program_name)
    else:
         print("和田さんが外出しました。")
         start_process(program_name)

# 予測されたクラスが "wada" 以外の場合にメッセージを送信。         
elif predicted_class != "wada":
    # 予測した人物をターミナルに確信度とクラス名を表示
    print(f"予測された人物は {predicted_class_jp} さんで、確信度は {percentage}% です。")
    
    # 送信するメッセージを作成
    message = f"予測された人物は {predicted_class_jp} さんで、確信度は {percentage}% です。"
    # タイムスタンプを追加
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    message_with_timestamp = f"{message} (撮影日時: {timestamp})"

    # LINE Notifyでメッセージを送信する関数を定義
    def send_line_notify_with_message(notification_message):
        headers = {
            'Authorization': f'Bearer {line_notify_token}'
        }
        payload = {
            'message': notification_message,
        }
        files = {'imageFile': open(image_path, 'rb')}
        requests.post('https://notify-api.line.me/api/notify', headers=headers, data=payload, files=files)

    # LINE Notifyでメッセージを送信
    #send_line_notify_with_message(message_with_timestamp)
