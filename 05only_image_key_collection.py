import os
import sys
import serial
import time
import tty
import termios
import cv2
import threading
import csv

# 스크립트의 디렉토리를 현재 작업 디렉토리로 변경
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(script_dir)

print("Current working directory:", os.getcwd())

# 시리얼 포트 설정 
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # 아두이노 초기화를 위한 대기 시간

# 데이터 저장 폴더와 파일 설정
data_folder = 'data'
try:
    os.makedirs(data_folder, exist_ok=True)
    print(f"Data folder created at: {os.path.abspath(data_folder)}")
except Exception as e:
    print(f"Error creating data folder: {e}")

csv_file = os.path.join(data_folder, 'dataset.csv')

# CSV 파일 초기화
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp', 'image_path', 'command'])

frame_count = 0
running = True
collecting_data = False
command = ''
lock = threading.Lock()
last_command_time = 0
last_key = None

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
    global running, command, collecting_data, last_command_time, last_key
    while running:
        key = getKey()
        if key == '1':
            collecting_data = True
            last_key = None
            print("Ready to collect data")
        elif key == '2' or key == 'q':
            collecting_data = False
            print("Data collection stopped")
            if key == 'q':
                command = 'S'
                running = False
        else:
            last_key = key
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

            with lock:
                ser.write(command.encode())
            print(f"Command: {command}")

# 데이터를 저장하는 함수
def save_data():
    global command, collecting_data, last_command_time, last_key
    while running:
        if collecting_data and last_key and (time.time() - last_command_time >= 0.5):
            last_command_time = time.time()
            timestamp = int(time.time() * 1000)
            image_path = os.path.join(data_folder, f'image_{timestamp}.jpg')
            ret, video = cap.read()
            if ret:
                video = cv2.flip(video, 1)
                cv2.imwrite(image_path, video)
                with open(csv_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([timestamp, image_path, command])
            print(f"Saved: {image_path}, Command: {command}")
        time.sleep(0.1)

# 카메라 초기화
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# 키보드 입력을 처리하는 스레드 시작
key_thread = threading.Thread(target=handle_keys)
key_thread.start()

# 데이터를 저장하는 스레드 시작
data_thread = threading.Thread(target=save_data)
data_thread.start()

try:
    while running:
        ret, video = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        video = cv2.flip(video, 1)
        cv2.imshow("image", video)

        # ESC 키를 누르면 루프 종료
        if cv2.waitKey(1) & 0xFF == 27:  # ESC 키
            running = False

finally:
    # 정리 작업
    cap.release()
    cv2.destroyAllWindows()
    ser.close()
    key_thread.join()
    data_thread.join()