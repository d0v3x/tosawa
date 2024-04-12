import requests
import time

def send_line_notify(message):
    line_notify_token = 'AMRkehZHu6zyWtFB1DvBPlsqgRSRESgRlr5LN4Hxl5G'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    payload = {'message': message}
    requests.post(line_notify_api, headers=headers, data=payload)

def main():
    start_time = time.time()
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= 60:
            send_line_notify("和田さんが外出してから1時間が経過しました。055-xxx-xxxに通報しますか？")
            break
        time.sleep(1)

if __name__ == "__main__":
    main()
