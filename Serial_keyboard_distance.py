import serial
import time
import sys
import tty
import termios
import cv2
import threading

# # 시리얼 포트 설정 (아두이노와 연결된 포트 설정)
# ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
# time.sleep(2)  # 포트 안정화 대기
# print("Serial port opened successfully")

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

distance = "N/A11"
lock = threading.Lock()
def read_distance():
    global distance
    while True:
        if ser.is_open:
            if ser.in_waiting > 0:
                try:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    print(f"Received line: {line}")  # 디버그를 위해 읽은 데이터 출력
                    with lock:
                        distance = line
                    print(f"Updated distance: {distance}")  # 거리값 업데이트 확인
                except UnicodeDecodeError:
                    with lock:
                        distance = "N/A"
                except serial.SerialException as e:
                    print(f"Serial error: {e}")
                    with lock:
                        distance = "N/A"
            else:
                time.sleep(0.1)  # 시리얼 데이터가 없을 때 대기
        else:
            print("Serial port is closed.")
            break

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
    
    print(f"Current distance: {current_distance}")  # 디버깅을 위해 추가
    
    # 거리 값을 화면에 표시
    cv2.putText(frame, f"Distance: {distance} cm", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)        
    cv2.imshow("Fire Detection", frame)

    # 키 입력 처리
    key = cv2.waitKey(30) & 0xFF
    if key == 27:  # ESC 키를 누르면 종료
        break
    elif key == ord('w'):
        ser.write(b'F')  # Forward
        print("Sent command: F")
    elif key == ord('s'):
        ser.write(b'B')  # Backward
        print("Sent command: B")        
    elif key == ord('a'):
        ser.write(b'L')  # Move Left
        print("Sent command: L")        
    elif key == ord('d'):
        ser.write(b'R')  # Move Right
        print("Sent command: R")
    elif key == ord('q'):
        ser.write(b'T')  # Rotate Left
        print("Sent command: T")
    elif key == ord('e'):
        ser.write(b'Y')  # Rotate Right
        print("Sent command: Y")
    elif key == ord('z'):
        ser.write(b'Q')  # Move Left Forward
        print("Sent command: Q")
    elif key == ord('c'):
        ser.write(b'E')  # Move Right Forward
        print("Sent command: E")
    elif key == ord('u'):
        ser.write(b'Z')  # Move Left Backward
        print("Sent command: Z")
    elif key == ord('o'):
        ser.write(b'C')  # Move Right Backward
        print("Sent command: C")
    elif key == ord('x'):
        ser.write(b'S')  # Stop
        print("Sent command: S")
    elif key == ord('i'):
        ser.write(b'U')  # Servo1 Up
        print("Sent command: U")
    elif key == ord('k'):
        ser.write(b'D')  # Servo1 Down
        print("Sent command: D")
    elif key == ord('j'):
        ser.write(b'I')  # Servo2 Up
        print("Sent command: I")
    elif key == ord('l'):
        ser.write(b'K')  # Servo2 Down
        print("Sent command: K")
    elif key == ord('m'):
        ser.write(b'A')  # Activate Relay
        print("Sent command: A")
    elif key == ord('n'):
        ser.write(b'V')  # Deactivate Relay
        print("Sent command: V")
    elif key == ord('q'):
        ser.write(b'S')  # Stop before quitting
        print("Sent command: S")        
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
ser.close()
