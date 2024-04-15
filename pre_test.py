# これは推論テスト用プログラムです。
import serial
import time
import subprocess
import datetime
import requests
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential, Model,load_model
from PIL import Image
import sys
import argparse
import random
import time
import cv2

# カメラバッファの数
CAMERA_BUF_FLUSH_NUM = 6

# クラス定義
class_names = {
    "wada": "和田",
    "sano": "佐野",
    "tomioka": "冨岡"
}

# VGG16用のリサイズ解像度
image_size = 224

# モデルのロード tosawa_face_v6が最新
print('モデルのロード...')
model = load_model('./tosawa_face_v6.h5')

# ビデオカメラ開始
print('ビデオカメラ開始...')
cap = cv2.VideoCapture(1)

# OpenCVのチックメータ（ストップウオッチ）機能をtmという名前で使えるようにする
tm = cv2.TickMeter()

while True:
    #バッファに滞留しているカメラ画像を指定回数読み飛ばし、最新画像をframeに読み込む
    for i in range(CAMERA_BUF_FLUSH_NUM):
        ret, frame = cap.read()
    
    # 取り込んだ画像の幅を縦横比を維持して500ピクセルに縮小
    ratio = 500 / frame.shape[1]
    frame = cv2.resize(frame, dsize=None, fx=ratio, fy=ratio)

    # 指定した大きさにリサイズする。
    #dst = cv2.resize(frame, dsize=(500, 500))
    frame =  frame[0 : 375, 62: 437]
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    
    #nanpy array にimage array を引き継ぐ
    pil_image_color = Image.fromarray(image)
    
    #推論モデルの224×224サイズにリサイズする
    pil_image_color = pil_image_color.resize((image_size,image_size))
    #RGBの256階調を0～1階調に変換
    data = np.asarray(pil_image_color) / 255.0
    X = []
    X.append(data)
    X = np.array(X)
    #推論 VGG16モデルを動かす
    result = model.predict([X])[0]
    predicted_class_index = result.argmax()
    percentage = int(result[predicted_class_index] * 100)
    predicted_class = list(class_names.keys())[predicted_class_index]
    predicted_class_jp = class_names[predicted_class]
    ##画面描画文字編集
    outText = "pre:"
    outText = outText + str(predicted_class) 
    outText = outText + ','
    outText = outText + str(percentage) + '%'
    ##コマンドプロンプトにoutTextを表示
    print(outText)
    ##フィードバックframe画面にoutTextを入れ込む
    cv2.putText(frame,
            outText,
            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), thickness=2)
    # フレームを画面に描画
    cv2.imshow('Live', frame)
    ##50mSec Waitする
    if cv2.waitKey(50) >= 0:
        print(cv2.waitKey(50))
    time.sleep(0.5)
ser.close()
print('終了処理...')
cv2.destroyAllWindows()
cap.release()
time.sleep(3)

