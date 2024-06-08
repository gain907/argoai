#include <Servo.h>
#include <AFMotor.h>
#include <SoftwareSerial.h> 

// 모터 정의
AF_DCMotor motor1(1);  // 모터 쉴드 M1 연결
AF_DCMotor motor2(2);  // 모터 쉴드 M2 연결
AF_DCMotor motor3(3);  // 모터 쉴드 M3 연결
AF_DCMotor motor4(4);  // 모터 쉴드 M4 연결

// 서보 모터 정의
Servo servo1;
Servo servo2;

int servo1Pos, servo2Pos;
int speedDelay = 20;

// 모터 속도 및 방향 상태 변수
int motor1Speed = 80;
int motor2Speed = 80;
int motor3Speed = 80;
int motor4Speed = 80;

char motor1Direction = 'S'; // S: Stop, F: Forward, B: Backward
char motor2Direction = 'S';
char motor3Direction = 'S';
char motor4Direction = 'S';

// 릴레이 핀 정의
const int relayPin = 14;  // A0 = D14

void setup() {
  Serial.begin(9600);  // 시리얼 통신 시작

  servo1.attach(9);   // 서보 모터 1 핀
  servo2.attach(10);   // 서보 모터 2 핀
  servo1Pos = 90;
  servo2Pos = 90;  

  servo1.write(servo1Pos);
  servo2.write(servo2Pos);
  
  pinMode(relayPin, OUTPUT);  // 릴레이 출력 설정

  // 모터 속도 설정
  motor1.setSpeed(motor1Speed);
  motor2.setSpeed(motor2Speed);
  motor3.setSpeed(motor3Speed);
  motor4.setSpeed(motor4Speed);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    Serial.print("Command:");
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
      case 'U':
        moveServo1up();
        break;
      case 'D':
        moveServo1down();
        break;
      case 'I':
        moveServo2up();
        break;
      case 'K':
        moveServo2down();
        break;
      case 'A':
        activateRelay();
        break;
      case 'V':
        sleepRelay();
        break;
    }

    // 모터와 서보 모터 상태 전송
    Serial.print("M1:"); Serial.print(motor1Speed);
    Serial.print(",D1:"); Serial.print(motor1Direction);
    Serial.print(",M2:"); Serial.print(motor2Speed);
    Serial.print(",D2:"); Serial.print(motor2Direction);
    Serial.print(",M3:"); Serial.print(motor3Speed);
    Serial.print(",D3:"); Serial.print(motor3Direction);
    Serial.print(",M4:"); Serial.print(motor4Speed);
    Serial.print(",D4:"); Serial.print(motor4Direction);
    Serial.print(",S1:"); Serial.print(servo1Pos);
    Serial.print(",S2:"); Serial.println(servo2Pos);
  }
}

void moveForward() {
  motor1.run(FORWARD);
  motor2.run(FORWARD);
  motor3.run(FORWARD);
  motor4.run(FORWARD);
  motor1Direction = 'F';
  motor2Direction = 'F';
  motor3Direction = 'F';
  motor4Direction = 'F';
}

void moveBackward() {
  motor1.run(BACKWARD);
  motor2.run(BACKWARD);
  motor3.run(BACKWARD);
  motor4.run(BACKWARD);
  motor1Direction = 'B';
  motor2Direction = 'B';
  motor3Direction = 'B';
  motor4Direction = 'B';
}

void moveSidewaysLeft() {
  motor1.run(BACKWARD);
  motor2.run(FORWARD);
  motor3.run(FORWARD);
  motor4.run(BACKWARD);
  motor1Direction = 'B';
  motor2Direction = 'F';
  motor3Direction = 'F';
  motor4Direction = 'B';
}

void moveSidewaysRight() {
  motor1.run(FORWARD);
  motor2.run(BACKWARD);
  motor3.run(BACKWARD);
  motor4.run(FORWARD);
  motor1Direction = 'F';
  motor2Direction = 'B';
  motor3Direction = 'B';
  motor4Direction = 'F';
}

void moveLeftForward() {
  motor1.run(RELEASE);
  motor2.run(FORWARD);
  motor3.run(FORWARD);
  motor4.run(RELEASE);
  motor1Direction = 'S';
  motor2Direction = 'F';
  motor3Direction = 'F';
  motor4Direction = 'S';
}

void moveRightForward() {
  motor1.run(FORWARD);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(FORWARD);
  motor1Direction = 'F';
  motor2Direction = 'S';
  motor3Direction = 'S';
  motor4Direction = 'F';
}

void moveLeftBackward() {
  motor1.run(BACKWARD);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(BACKWARD);
  motor1Direction = 'B';
  motor2Direction = 'S';
  motor3Direction = 'S';
  motor4Direction = 'B';
}

void moveRightBackward() {
  motor1.run(RELEASE);
  motor2.run(BACKWARD);
  motor3.run(BACKWARD);
  motor4.run(RELEASE);
  motor1Direction = 'S';
  motor2Direction = 'B';
  motor3Direction = 'B';
  motor4Direction = 'S';
}

void rotateLeft() {
  motor1.run(BACKWARD);
  motor2.run(FORWARD);
  motor3.run(BACKWARD);
  motor4.run(FORWARD);
  motor1Direction = 'B';
  motor2Direction = 'F';
  motor3Direction = 'B';
  motor4Direction = 'F';
}

void rotateRight() {
  motor1.run(FORWARD);
  motor2.run(BACKWARD);
  motor3.run(FORWARD);
  motor4.run(BACKWARD);
  motor1Direction = 'F';
  motor2Direction = 'B';
  motor3Direction = 'F';
  motor4Direction = 'B';
}

void stop() {
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(RELEASE);
  motor1Direction = 'S';
  motor2Direction = 'S';
  motor3Direction = 'S';
  motor4Direction = 'S';
}

void moveServo1up() {
  servo1Pos++;
  servo1.write(servo1Pos);
  delay(speedDelay);
}

void moveServo1down() {
  servo1Pos--;
  servo1.write(servo1Pos);
  delay(speedDelay);
}

void moveServo2up() {
  servo2Pos++;
  servo2.write(servo2Pos);
  delay(speedDelay);
}

void moveServo2down() {
  servo2Pos--;
  servo2.write(servo2Pos);
  delay(speedDelay);
}

void activateRelay() {
  digitalWrite(relayPin, HIGH);
}

void sleepRelay() {
  digitalWrite(relayPin, LOW);
}
