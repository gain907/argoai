#include <Servo.h>

Servo servo01;
Servo servo02;
Servo servo03;
Servo servo04;
Servo servo05;
Servo servo06;

int servo1Pos, servo2Pos, servo3Pos, servo4Pos, servo5Pos, servo6Pos; // current position
int speedDelay = 20;
int m = 0;

void setup() {
  servo01.attach(4);
  servo02.attach(5);
  servo03.attach(6);
  servo04.attach(7);
  servo05.attach(8);
  servo06.attach(9);
  Serial.begin(9600);

  servo1Pos = 90;
  servo01.write(servo1Pos);
  servo2Pos = 90;
  servo02.write(servo2Pos);
  servo3Pos = 90;
  servo03.write(servo3Pos);
  servo4Pos = 95;
  servo04.write(servo4Pos);
  servo5Pos = 90;
  servo05.write(servo5Pos);
  servo6Pos = 90;
  servo06.write(servo6Pos);
}

void loop() {
  if (Serial.available() > 0) {
    char dataIn = Serial.read();

    if (dataIn == 'w') {
      servo1Pos++;
      servo01.write(servo1Pos);
      Serial.print("s1 증가 :");
      Serial.println(servo1Pos);
    } else if (dataIn == 's') {
      servo1Pos--;
      servo01.write(servo1Pos);
      Serial.print("s1 감소 :");
      Serial.println(servo1Pos);
    } else if (dataIn == 'e') {
      servo2Pos++;
      servo02.write(servo2Pos);
      Serial.print("s2 증가 :");
      Serial.println(servo2Pos);
    } else if (dataIn == 'd') {
      servo2Pos--;
      servo02.write(servo2Pos);
      Serial.print("s2 감소 :");
      Serial.println(servo2Pos);
    } else if (dataIn == 'r') {
      servo3Pos++;
      servo03.write(servo3Pos);
      Serial.print("s3 증가 :");
      Serial.println(servo3Pos);
    } else if (dataIn == 'f') {
      servo3Pos--;
      servo03.write(servo3Pos);
      Serial.print("s3 감소 :");
      Serial.println(servo3Pos);
    } else if (dataIn == 't') {
      servo4Pos++;
      servo04.write(servo4Pos);
      Serial.print("s4 증가 :");
      Serial.println(servo4Pos);
    } else if (dataIn == 'g') {
      servo4Pos--;
      servo04.write(servo4Pos);
      Serial.print("s4 감소 :");
      Serial.println(servo4Pos);
    } else if (dataIn == 'y') {
      servo5Pos++;
      servo05.write(servo5Pos);
      Serial.print("s5 증가 :");
      Serial.println(servo5Pos);
    } else if (dataIn == 'h') {
      servo5Pos--;
      servo05.write(servo5Pos);
      Serial.print("s5 감소 :");
      Serial.println(servo5Pos);
    } else if (dataIn == 'u') {
      servo6Pos++;
      servo06.write(servo6Pos);
      Serial.print("s6 증가 :");
      Serial.println(servo6Pos);
    } else if (dataIn == 'j') {
      servo6Pos--;
      servo06.write(servo6Pos);
      Serial.print("s6 감소 :");
      Serial.println(servo6Pos);
    } else if (dataIn == 'b') {
      basic_smooth();
    }
  }
}

void basic_smooth() {
  moveServo(servo01, servo1Pos, 90);
  moveServo(servo02, servo2Pos, 90);
  moveServo(servo03, servo3Pos, 90);
  moveServo(servo04, servo4Pos, 95);
  moveServo(servo05, servo5Pos, 90);
  moveServo(servo06, servo6Pos, 90);
}

void moveServo(Servo& servo, int& currentPos, int targetPos) {
  if (currentPos < targetPos) {
    for (; currentPos <= targetPos; currentPos++) {
      servo.write(currentPos);
      delay(15);
    }
  } else {
    for (; currentPos >= targetPos; currentPos--) {
      servo.write(currentPos);
      delay(15);
    }
  }
}
