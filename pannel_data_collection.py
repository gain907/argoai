import os
import csv
import serial
import time
import sys
import tty
import termios
import cv2
import threading

def init_serial():
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        time.sleep(2)  # 아두이노 초기화를 위한 대기 시간
        return ser
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return None

ser = init_serial()
if ser is None:
    print("Failed to initialize serial port.")
    exit()

# 카메라 초기화
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# 데이터 저장 폴더와 파일 설정
data_folder = 'data'
os.makedirs(data_folder, exist_ok=True)
csv_file = os.path.join(data_folder, 'dataset.csv')

# CSV 파일 초기화
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['image_path', 'M1', 'D1', 'M2', 'D2', 'M3', 'D3', 'M4', 'D4', 'S1', 'S2', 'command'])

frame_count = 0
running = True

def getKey():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key

def handle_keys():
    global running
    while running:
        key = getKey()
        command = ''
        if key == 'w':
            command = 'F'
        elif key == 's':
            command = 'B'
        elif key == 'a':
            command = 'L'
        elif key == 'd':
            command = 'R'
        elif key == 'q':
            command = 'T'
        elif key == 'e':
            command = 'Y'
        elif key == 'z':
            command = 'Q'
        elif key == 'c':
            command = 'E'
        elif key == 'u':
            command = 'Z'
        elif key == 'o':
            command = 'C'
        elif key == 'x':
            command = 'S'
        elif key == 'i':
            command = 'U'
        elif key == 'k':
            command = 'D'
        elif key == 'j':
            command = 'I'
        elif key == 'l':
            command = 'K'
        elif key == 'm':
            command = 'A'
        elif key == 'n':
            command = 'V'
        elif key == 'q':
            command = 'S'
            running = False
            break

        if command:
            ser.write(command.encode())
            # 명령을 파일에 기록
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([image_path, motor1_speed, motor1_dir, motor2_speed, motor2_dir, motor3_speed, motor3_dir, motor4_speed, motor4_dir, servo1_angle, servo2_angle, command])

key_thread = threading.Thread(target=handle_keys)
key_thread.start()

try:
    while running:
        # 카메라 프레임 읽기
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # 이미지 파일 저장
        image_path = os.path.join(data_folder, f'image_{frame_count}.jpg')
        cv2.imwrite(image_path, frame)

        # 아두이노 데이터 읽기
        if ser.in_waiting > 0:
            try:
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
                        writer.writerow([image_path, motor1_speed, motor1_dir, motor2_speed, motor2_dir, motor3_speed, motor3_dir, motor4_speed, motor4_dir, servo1_angle, servo2_angle])

                    frame_count += 1
            except Exception as e:
                print(f"Error reading from serial port: {e}")

        # ESC 키를 누르면 루프 종료
        if cv2.waitKey(1) & 0xFF == 27:  # ESC 키
            running = False
            break

        # 카메라 영상 표시
        cv2.imshow("image", frame)

finally:
    # 정리 작업
    cap.release()
    cv2.destroyAllWindows()
    ser.close()
