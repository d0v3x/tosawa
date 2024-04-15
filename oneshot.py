# 外付けカメラの場合は撮影に3秒ほどディレイがかかる
import cv2
import subprocess

# 推論プログラムのパス 
file_path = "/home/pi/ai101/predict_new.py"

# 解像度を設定
width = 1024
height = 1024

# VideoCaptureオブジェクトを作成し、カメラからのストリームを取得
cap = cv2.VideoCapture(1)

# 解像度を設定
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# カメラからのフレームを読み込む
ret, frame = cap.read()

# フレームを保存
cv2.imwrite('image.jpg', frame)

# カメラを解放
cap.release()

# 正常に処理が終了した場合のターミナル表示
print("正常に撮影が終了しました。")
print("推論フェーズに移ります。")

# 撮影した画像を引数に推論プログラムの起動
subprocess.call(['python', file_path, 'image.jpg'])
