int ledPin = 13;

void setup() {
  // 13? ?? ???? ??
  pinMode(ledPin, OUTPUT);
  // ?? ?? ??
  Serial.begin(9600);
}

void loop() {
  // ?? ??? ???? ??? ??
  if (Serial.available() > 0) {
    // ???? ??
    char command = Serial.read();
    
    // '1'? ??? LED ??
    if (command == '1') {
      digitalWrite(ledPin, HIGH);
    }
    // '0'? ??? LED ??
    else if (command == '0') {
      digitalWrite(ledPin, LOW);
    }
  }
}
