# 外出60秒後にLINEで通知するプログラム
import requests
import time

# LINEの送信内容定義
def send_line_notify(message):
    line_notify_token = 'Your token'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    payload = {'message': message}
    requests.post(line_notify_api, headers=headers, data=payload)
    
# メインループの定義
def main():
    start_time = time.time()
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= 60:
            send_line_notify("和田さんが外出してから1時間が経過しました。055-xxx-xxxに通報しますか？")
            print("和田さんが外出してから1時間が経過したので、通報用のLINEを送信しました。")
            break
        time.sleep(1)

if __name__ == "__main__":
    main()
