#include <Servo.h>
#include <AFMotor.h>
#include <SoftwareSerial.h>

// ?? ??
AF_DCMotor motor1(1);  // ?? ?? M1 ??
AF_DCMotor motor2(2);  // ?? ?? M2 ??
AF_DCMotor motor3(3);  // ?? ?? M3 ??
AF_DCMotor motor4(4);  // ?? ?? M4 ??

// ?? ?? ??
Servo servo1;
Servo servo2;

int servo1Pos = 90;
int servo2Pos = 90;
int speedDelay = 20;

// ??? ? ??
const int relayPin = 14;  // A0 = D14

void setup() {
  Serial.begin(9600);  // ??? ?? ??

  servo1.attach(9);   // ?? ?? 1 ?
  servo2.attach(10);  // ?? ?? 2 ?
  servo1.write(servo1Pos);
  servo2.write(servo2Pos);
  
  pinMode(relayPin, OUTPUT);  // ??? ?? ??

  // ?? ?? ??
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
        // ??? ?? ?? ?? ??
    Serial.print("M1:"); Serial.print(motor1.getSpeed());
    Serial.print(",D1:"); Serial.print((motor1.getDirection() == FORWARD) ? "F" : "B");
    Serial.print(",M2:"); Serial.print(motor2.getSpeed());
    Serial.print(",D2:"); Serial.print((motor2.getDirection() == FORWARD) ? "F" : "B");
    Serial.print(",M3:"); Serial.print(motor3.getSpeed());
    Serial.print(",D3:"); Serial.print((motor3.getDirection() == FORWARD) ? "F" : "B");
    Serial.print(",M4:"); Serial.print(motor4.getSpeed());
    Serial.print(",D4:"); Serial.print((motor4.getDirection() == FORWARD) ? "F" : "B");
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

void moveServo1up(Servo servo) {
  servo1Pos++;
  servo.write(servo1Pos);
  Serial.println("??1 ?? :");
  Serial.println(servo1Pos);
  delay(speedDelay);
}

void moveServo1down(Servo servo) {
  servo1Pos--;
  servo.write(servo1Pos);
  Serial.print("??1 ?? :");
  Serial.println(servo1Pos);
  delay(speedDelay);
}

void moveServo2up(Servo servo) {
  servo2Pos++;
  servo.write(servo2Pos);
  Serial.println("??2 ?? :");
  Serial.println(servo2Pos);
  delay(speedDelay);
}

void moveServo2down(Servo servo) {
  servo2Pos--;
  servo.write(servo2Pos);
  Serial.print("??2 ?? :");
  Serial.println(servo2Pos);
  delay(speedDelay);
}

void activateRelay() {
  digitalWrite(relayPin, HIGH);
}

void sleepRelay() {
  digitalWrite(relayPin, LOW);
}
