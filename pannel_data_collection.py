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
    writer.writerow(['timestamp', 'image_path', 'M1_speed', 'M1_dir', 'M2_speed', 'M2_dir', 'M3_speed', 'M3_dir', 'M4_speed', 'M4_dir', 'S1_angle', 'S2_angle', 'command'])

frame_count = 0
running = True
collecting_data = False
command = ''
lock = threading.Lock()

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
        if key == '1':
            collecting_data = True  # 데이터 수집 시작
            print("Data collection started")
        elif key == '2'
