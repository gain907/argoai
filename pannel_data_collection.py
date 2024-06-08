import serial
import time
import sys
import tty
import termios
import cv2
import threading
import os
import csv

# 현재 작업 디렉토리 확인
print("Current working directory:", os.getcwd())

# 시리얼 포트 설정
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # 아두이노 초기화를 위한 대기 시간

# 데이터 저장 폴더와 파일 설정
data_folder = '/home/argo/myenv/data'
try:
    os.makedirs(data_folder, exist_ok=True)
    print(f"Data folder created at: {os.path.abspath(data_folder)}")
except Exception as e:
    print(f"Error creating data folder: {e}")

csv_file = os.path.join(data_folder, 'dataset.csv')

# CSV 파일 초기화
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp', 'image_path', 'M1_speed', 'M1_dir', 'M2_speed', 'M2_dir', 'M3_speed', 'M3_dir', 'M4_speed', 'M4_dir', 'S1_angle', 'S2_angle', 'command'])

frame_count = 0
running = True
collecting_data = False
command = ''

# 키보드 입력 함수
def getKey():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key

# 키보드 입력을 처리하는 함수
def handle_keys():
    global running, frame_count, command, collecting_data
    while running:
        key = getKey()
        if key == 'w':
            command = 'F'  # Forward
        elif key == 's':
            command = 'B'  # Backward
        elif key == 'a':
            command = 'L'  # Move Left
        elif key == 'd':
            command = 'R'  # Move Right
        elif key == 'q':
            command = 'T'  # Rotate Left
        elif key == 'e':
            command = 'Y'  # Rotate Right
        elif key == 'z':
            command = 'Q'  # Move Left Forward
        elif key == 'c':
            command = 'E'  # Move Right Forward
        elif key == 'u':
            command = 'Z'  # Move Left Backward
        elif key == 'o':
            command = 'C'  # Move Right Backward
        elif key == 'x':
            command = 'S'  # Stop
        elif key == 'i':
            command = 'U'  # Servo1 Up
        elif key == 'k':
            command = 'D'  # Servo1 Down
        elif key == 'j':
            command = 'I'  # Servo2 Up
        elif key == 'l':
            command = 'K'  # Servo2 Down
        elif key == 'm':
            command = 'A'  # Activate Relay
        elif key == 'n':
            command = 'V'  # Deactivate Relay
        elif key == 'q':
            command = 'S'  # Stop before quitting
            running = False
            break

        if command:
            ser.write(command.encode())
            collecting_data = True

# 카메라 초기화
cap = cv2.VideoCapture(0, cv2.CAP_V4L)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# 키보드 입력을 처리하는 스레드 시작
key_thread = threading.Thread(target=handle_keys)
key_thread.start()

last_collection_time = time.time()

try:
    while running:
        current_time = time.time()
        if collecting_data and (current_time - last_collection_time >= 0.5):
            last_collection_time = current_time

            # 카메라 프레임 캡처 및 저장
            ret, frame = cap.read()
            if ret:
                timestamp = int(time.time())
                image_path = os.path.join(data_folder, f'image_{timestamp}.jpg')
                cv2.imwrite(image_path, frame)

                # 아두이노 데이터 읽기
                if ser.in_waiting > 0:
                    arduino_data = ser.readline().decode('utf-8').strip()
                    print(arduino_data)  # 데이터 확인용 출력

                    # 데이터 파싱
                    data_parts = arduino_data.split(',')
                    if len(data_parts) == 12:
                        motor1_speed = data_parts[0].split(':')[1]
                        motor1_dir = data_parts[1].split(':')[1]
                        motor2_speed = data_parts[2].split(':')[1]
                        motor2_dir = data_parts[3].split(':')[1]
                        motor3_speed = data_parts[4].split(':')[1]
                        motor3_dir = data_parts[5].split(':')[1]
                        motor4_speed = data_parts[6].split(':')[1]
                        motor4_dir = data_parts[7].split(':')[1]
                        servo1_angle = data_parts[8].split(':')[1]
                        servo2_angle = data_parts[9].split(':')[1]

                        # CSV 파일에 데이터 저장
                        with open(csv_file, mode='a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([timestamp, image_path, motor1_speed, motor1_dir, motor2_speed, motor2_dir, motor3_speed, motor3_dir, motor4_speed, motor4_dir, servo1_angle, servo2_angle, command])

                        frame_count += 1

    # ESC 키를 누르면 루프 종료
    if cv2.waitKey(1) & 0xFF == 27:  # ESC 키
        running = False

finally:
    # 정리 작업
    cap.release()
    cv2.destroyAllWindows()
    ser.close()
