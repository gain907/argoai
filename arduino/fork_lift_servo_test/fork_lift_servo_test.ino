#include <Servo.h>

// 서보모터 객체 생성
Servo myServo;

// 서보모터 제어 핀 정의
const int servoPin = 10;
int angle = 90;  // 서보모터 초기 각도 설정

// 설정 함수
void setup() {
  // 서보모터 핀 연결
  myServo.attach(servoPin);
  myServo.write(angle); // 초기 각도 설정
  // 시리얼 통신 시작
  Serial.begin(9600);
  Serial.println("서보모터 제어 시작: 'i' - 각도 증가, 'd' - 각도 감소, 's' - 정지");
}

// 메인 루프
void loop() {
  // 시리얼 입력 확인
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    // 명령에 따른 동작 수행
    if (command == 'i') {
      // 각도 증가 (최대 180도)
      angle += 5;
      if (angle > 180) {
        angle = 180;
      }
      myServo.write(angle);
      Serial.print("각도 증가: ");
      Serial.println(angle);
      
    } else if (command == 'd') {
      // 각도 감소 (최소 0도)
      angle -= 5;
      if (angle < 0) {
        angle = 0;
      }
      myServo.write(angle);
      Serial.print("각도 감소: ");
      Serial.println(angle);
      
    } else if (command == 's') {
      // 서보모터 정지 (현재 각도 유지)
      myServo.write(angle);
      Serial.println("정지");
    }
  }
}
