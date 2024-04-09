import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import sys
import datetime
import requests

class_names = {
    "pink": "ピンク",
    "green": "グリーン"
    "blue": "ブルー"
    "black": "ブラック"
}

image_size = 224

# 画像を読み込む
image_path = sys.argv[1]
image = Image.open(image_path)
image = image.convert("RGB")
image = image.resize((image_size, image_size))
data = np.asarray(image) / 255.0
X = []
X.append(data)
X = np.array(X)

# モデルを読み込む
model = load_model('./tosawa_v2.h5')

# 予測を行う
result = model.predict([X])[0]
predicted_class_index = result.argmax()
percentage = int(result[predicted_class_index] * 100)
predicted_class = list(class_names.keys())[predicted_class_index]
predicted_class_jp = class_names[predicted_class]

# LINE Notifyのアクセストークンを設定
line_notify_token = 'AMRkehZHu6zyWtFB1DvBPlsqgRSRESgRlr5LN4Hxl5G'

# 予測されたクラスが "pink" または "green" の場合にメッセージを送信
if predicted_class in class_names:
    # 送信するメッセージを作成
    message = f"予測された人物は {predicted_class_jp} さんで、確信度は {percentage}% です。"
    # タイムスタンプを追加
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    message_with_timestamp = f"{message} (撮影日時: {timestamp})"

    # LINE Notifyで画像を送信する関数を定義
    def send_line_notify_with_image(notification_message, image_path):
        headers = {
            'Authorization': f'Bearer {line_notify_token}'
        }
        payload = {
            'message': notification_message,
        }
        files = {'imageFile': open(image_path, 'rb')}
        requests.post('https://notify-api.line.me/api/notify', headers=headers, data=payload, files=files)

    # LINE Notifyでメッセージと画像を送信
    send_line_notify_with_image(message_with_timestamp, image_path)
    print("LINEの送信が完了しました。")
