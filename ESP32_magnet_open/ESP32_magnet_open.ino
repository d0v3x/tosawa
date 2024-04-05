const int sensorPin = 32;  // 磁気センサーのピン
const int ledPin = 25;    // LEDのピン

int sensorState = 0;      // 磁気センサーの状態を保持する変数
int previousSensorState = 0;  // 前回の磁気センサーの状態を保持する変数

void setup() {
  pinMode(sensorPin, INPUT);  // 磁気センサーのピンを入力モードに設定
  pinMode(ledPin, OUTPUT);    // LEDのピンを出力モードに設定
  Serial.begin(115200);         // シリアル通信の開始
}

void loop() {
  // 磁気センサーの状態を読み取る
  sensorState = digitalRead(sensorPin);

  // 磁気センサーの状態が変化した場合
  if (sensorState != previousSensorState) {
    // 磁気センサーが離れた場合
    if (sensorState == 1) {
      Serial.println(sensorState);
      digitalWrite(ledPin, LOW);  // LEDを点灯
    } else {  // 磁気センサーが近づいた場合
      digitalWrite(ledPin, HIGH);   // LEDを消灯
      Serial.println(sensorState);
    }
    previousSensorState = sensorState;  // 前回の状態を更新
  }
}
