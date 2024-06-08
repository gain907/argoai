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

// 릴레이 핀 정의
const int relayPin = 14;  // A0 = D14

void setup() {
  Serial.begin(9600);  // 시리얼 통신 시작

  servo1.attach(9);   // 서보 모터 1 핀
  servo2.attach(10);  // 서보 모터 2 핀
  servo1Pos = 90;
  servo2Pos = 90;  

  servo1.write(servo1Pos);
  servo2.write(servo2Pos);
  
  pinMode(relayPin, OUTPUT);  // 릴레이 출력 설정

  // 모터 속도 설정
  motor1.setSpeed(80);
  motor2.setSpeed(80);
  motor3.setSpeed(80);
  motor4.setSpeed(80);
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
    Serial.print("M1:"); Serial.print(motor1.getSpeed());
    Serial.print(",D1:"); Serial.print(motor1.getDirection() == FORWARD ? "F" : motor1.getDirection() == BACKWARD ? "B" : "S");
    Serial.print(",M2:"); Serial.print(motor2.getSpeed());
    Serial.print(",D2:"); Serial.print(motor2.getDirection() == FORWARD ? "F" : motor2.getDirection() == BACKWARD ? "B" : "S");
    Serial.print(",M3:"); Serial.print(motor3.getSpeed());
    Serial.print(",D3:"); Serial.print(motor3.getDirection() == FORWARD ? "F" : motor3.getDirection() == BACKWARD ? "B" : "S");
    Serial.print(",M4:"); Serial.print(motor4.getSpeed());
    Serial.print(",D4:"); Serial.print(motor4.getDirection() == FORWARD ? "F" : motor4.getDirection() == BACKWARD ? "B" : "S");
    Serial.print(",S1:"); Serial.print(servo1Pos);
    Serial.print(",S2:"); Serial.println(servo2Pos);
  }
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
