// 핀 정의
const int ENA = 9;  // 디지털 핀 9 (PWM 신호)
const int IN1 = A0; // 아날로그 핀 A0 (디지털로 사용)
const int IN2 = A1; // 아날로그 핀 A1 (디지털로 사용)

// 설정 함수
void setup() {
  // 핀 모드 설정
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  
  // 시리얼 통신 시작
  Serial.begin(9600);
  Serial.println("지게차 제어 시작: 'u' - 위로, 'd' - 아래로, 's' - 정지");
}

// 메인 루프
void loop() {
  // 시리얼 입력 확인
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    // 명령에 따른 동작 수행
    if (command == 'u') {
      // 모터를 한 방향으로 회전 (위로)
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      analogWrite(ENA, 65); // 최대 속도
      Serial.println("위로 이동");
      
    } else if (command == 'd') {
      // 모터를 반대 방향으로 회전 (아래로)
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      analogWrite(ENA, 65); // 최대 속도
      Serial.println("아래로 이동");
      
    } else if (command == 's') {
      // 모터 정지
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      analogWrite(ENA, 0); // 정지
      Serial.println("정지");
    }
  }
}