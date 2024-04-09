import cv2

# VideoCaptureオブジェクトを作成し、カメラからのストリームを取得
cap = cv2.VideoCapture(0)

# カメラからのフレームを読み込む
ret, frame = cap.read()

# フレームを保存
cv2.imwrite('image.jpg', frame)

# カメラを解放
cap.release()

print("正常に撮影が終了しました。")
