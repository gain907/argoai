#include <Servo.h>
#include <AFMotor.h>
#include <SoftwareSerial.h>

// DC 모터 정의
AF_DCMotor motor1(1);  // 모터 쉴드 M1 연결
AF_DCMotor motor2(2);  // 모터 쉴드 M2 연결
AF_DCMotor motor3(3);  // 모터 쉴드 M3 연결
AF_DCMotor motor4(4);  // 모터 쉴드 M4 연결

// // 서보 모터 정의
// Servo myServo;  // 추가 서보 모터 정의

int speedDelay = 20;
// int angle = 110;  // 서보모터 초기 각도 설정
// 서보 모터 정의
const int servoPin = 10;  // 서보 모터 핀
int angle = 110;  // 서보모터 초기 각도 설정
unsigned long lastPulse = 0;


// TT 모터 핀 정의
const int ENA = 9;  // 디지털 핀 9 (PWM 신호)
const int IN1 = A0; // 아날로그 핀 A0 (디지털로 사용)
const int IN2 = A1; // 아날로그 핀 A1 (디지털로 사용)

void setup() {
  Serial.begin(9600);  // 시리얼 통신 시작

  // // 서보 모터 핀 연결
  // myServo.attach(10); // 추가 서보 모터 핀
  // myServo.write(angle); // 초기 각도 설정
  // 서보 모터 핀 설정
  pinMode(servoPin, OUTPUT);

  // TT 모터 핀 모드 설정
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  digitalWrite(ENA, LOW);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);

  // 모터 속도 설정
  motor1.setSpeed(150);
  motor2.setSpeed(150);
  motor3.setSpeed(150);
  motor4.setSpeed(150);

  Serial.println("제어 시작: 'F', 'B', 'L', 'R', 'Q', 'E', 'Z', 'C', 'T', 'Y', 'S', 'u', 'd', 's', 'i', 'k'");
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    Serial.print("명령어 입력: ");
    Serial.println(command);

    switch (command) {
      case 'F':
        moveForward();
        break;
      case 'B':
        moveBackward();
        break;
      case 'L':
        moveSidewaysLeft();
        break;
      case 'R':
        moveSidewaysRight();
        break;
      case 'Q':
        moveLeftForward();
        break;
      case 'E':
        moveRightForward();
        break;
      case 'Z':
        moveLeftBackward();
        break;
      case 'C':
        moveRightBackward();
        break;
      case 'T':
        rotateLeft();
        break;
      case 'Y':
        rotateRight();
        break;
      case 'S':
        stop();
        break;
      case 'u':
        moveTTMotorUp();
        break;
      case 'd':
        moveTTMotorDown();
        break;
      case 's':
        stopTTMotor();
        break;
      case 'i':
        increaseMyServoAngle();
        break;
      case 'k':
        decreaseMyServoAngle();
        break;
    }
  }
  // 서보 모터를 주기적으로 업데이트
  updateServo();  
}

void moveForward() {
  motor1.run(FORWARD);
  motor2.run(FORWARD);
  motor3.run(FORWARD);
  motor4.run(FORWARD);
}

void moveBackward() {
  motor1.run(BACKWARD);
  motor2.run(BACKWARD);
  motor3.run(BACKWARD);
  motor4.run(BACKWARD);
}

void moveSidewaysLeft() {
  motor1.run(BACKWARD);
  motor2.run(FORWARD);
  motor3.run(FORWARD);
  motor4.run(BACKWARD);
}

void moveSidewaysRight() {
  motor1.run(FORWARD);
  motor2.run(BACKWARD);
  motor3.run(BACKWARD);
  motor4.run(FORWARD);
}

void moveLeftForward() {
  motor1.run(RELEASE);
  motor2.run(FORWARD);
  motor3.run(FORWARD);
  motor4.run(RELEASE);
}

void moveRightForward() {
  motor1.run(FORWARD);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(FORWARD);
}

void moveLeftBackward() {
  motor1.run(BACKWARD);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(BACKWARD);
}

void moveRightBackward() {
  motor1.run(RELEASE);
  motor2.run(BACKWARD);
  motor3.run(BACKWARD);
  motor4.run(RELEASE);
}

void rotateLeft() {
  motor1.run(BACKWARD);
  motor2.run(FORWARD);
  motor3.run(BACKWARD);
  motor4.run(FORWARD);
}

void rotateRight() {
  motor1.run(FORWARD);
  motor2.run(BACKWARD);
  motor3.run(FORWARD);
  motor4.run(BACKWARD);
}

void stop() {
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(RELEASE);
}

void moveTTMotorUp() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 65); // 속도 설정
  Serial.println("위로 이동");
}

void moveTTMotorDown() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  analogWrite(ENA, 65); // 속도 설정
  Serial.println("아래로 이동");
}

void stopTTMotor() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 0); // 정지
  Serial.println("정지");
}

// void increaseMyServoAngle() {
//   angle += 5;
//   if (angle > 180) angle = 180;
//   myServo.write(angle);
//   Serial.print("각도 증가: ");
//   Serial.println(angle);
// }

// void decreaseMyServoAngle() {
//   angle -= 5;
//   if (angle < 0) angle = 0;
//   myServo.write(angle);
//   Serial.print("각도 감소: ");
//   Serial.println(angle);
// }
void increaseMyServoAngle() {
  angle += 5;
  if (angle > 180) angle = 180;
  Serial.print("각도 증가: ");
  Serial.println(angle);
}

void decreaseMyServoAngle() {
  angle -= 5;
  if (angle < 0) angle = 0;
  Serial.print("각도 감소: ");
  Serial.println(angle);
}

void updateServo() {
  unsigned long currentMillis = millis();
  if (currentMillis - lastPulse >= 20) {
    lastPulse = currentMillis;
    int pulseWidth = map(angle, 0, 180, 544, 2400); // 544us에서 2400us로 매핑
    digitalWrite(servoPin, HIGH);
    delayMicroseconds(pulseWidth);
    digitalWrite(servoPin, LOW);
  }
}