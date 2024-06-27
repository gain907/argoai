import serial
import time
import threading
import cv2

# 시리얼 포트 설정 (아두이노와 연결된 포트 설정)
try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    time.sleep(2)  # 포트 안정화 대기
    print("Serial port opened successfully")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

print("Use the following keys to control the RC car and servo motors:")
print("w: Move Forward, s: Move Backward, a: Move Left, d: Move Right")
print("q: Rotate Left, e: Rotate Right, z: Move Left Forward, c: Move Right Forward")
print("u: Move Left Backward, o: Move Right Backward, x: Stop")
print("i: Servo1 Up, k: Servo1 Down, j: Servo2 Up, l: Servo2 Down")
print("m: Activate Relay, n: Deactivate Relay")
print("Press 'q' to quit.")

# 카메라 설정
cap = cv2.VideoCapture(0, cv2.CAP_V4L)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

distance = "N/A"
direction = ""
lock = threading.Lock()

def read_distance():
    global distance
    while True:
        if ser.is_open:
            if ser.in_waiting > 0:
                try:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    with lock:
                        distance = line
                except Exception as e:
                    with lock:
                        distance = "N/A"
        time.sleep(0.1)

# 거리 값 읽기 스레드 시작
distance_thread = threading.Thread(target=read_distance)
distance_thread.daemon = True
distance_thread.start()

while True:
    # 카메라 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    frame = cv2.flip(frame, 1)
    
    # 동기화된 거리 값 읽기
    with lock:
        current_distance = distance
        current_direction = direction
    
    # 거리 값을 화면에 표시
    cv2.putText(frame, f"Distance: {current_distance} cm", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # 방향을 화면에 표시
    cv2.putText(frame, f"Direction: {current_direction}", (350, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Fire Detection", frame)

    # 키 입력 처리
    key = cv2.waitKey(30) & 0xFF
    if key == 27:  # ESC 키를 누르면 종료
        break
    elif key == ord('w'):
        ser.write(b'F')  # Forward
        direction = "Forward"
    elif key == ord('s'):
        ser.write(b'B')  # Backward
        direction = "Backward"        
    elif key == ord('a'):
        ser.write(b'L')  # Move Left
        direction = "Left"
    elif key == ord('d'):
        ser.write(b'R')  # Move Right
        direction = "Right"
    elif key == ord('q'):
        ser.write(b'T')  # Rotate Left
        direction = "Rotate Left"
    elif key == ord('e'):
        ser.write(b'Y')  # Rotate Right
        direction = "Rotate Right"
    elif key == ord('z'):
        ser.write(b'Q')  # Move Left Forward
        direction = "Left Forward"
    elif key == ord('c'):
        ser.write(b'E')  # Move Right Forward
        direction = "Right Forward"
    elif key == ord('u'):
        ser.write(b'Z')  # Move Left Backward
        direction = "Left Backward"
    elif key == ord('o'):
        ser.write(b'C')  # Move Right Backward
        direction = "Right Backward"
    elif key == ord('x'):
        ser.write(b'S')  # Stop
        direction = "Stop"
    elif key == ord('i'):
        ser.write(b'U')  # Servo1 Up
        direction = "Servo1 Up"
    elif key == ord('k'):
        ser.write(b'D')  # Servo1 Down
        direction = "Servo1 Down"
    elif key == ord('j'):
        ser.write(b'I')  # Servo2 Up
        direction = "Servo2 Up"
    elif key == ord('l'):
        ser.write(b'K')  # Servo2 Down
        direction = "Servo2 Down"
    elif key == ord('m'):
        ser.write(b'A')  # Activate Relay
        direction = "Relay On"
    elif key == ord('n'):
        ser.write(b'V')  # Deactivate Relay
        direction = "Relay Off"

# 자원 해제
cap.release()
cv2.destroyAllWindows()
ser.close()
