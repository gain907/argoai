import serial
import time
import sys
import tty
import termios
import cv2
import threading

# ??? ?? ?? (????? ??? ??? ??)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # ???? ???? ?? ?? ??

# ? ??? ?? ??
def getKey():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key

# ? ??? ???? ??? ??
def handle_keys():
    global running
    while running:
        key = getKey()
        if key == 'w':
            ser.write(b'F')  # Forward
        elif key == 's':
            ser.write(b'B')  # Backward
        elif key == 'a':
            ser.write(b'L')  # Move Left
        elif key == 'd':
            ser.write(b'R')  # Move Right
        elif key == 'q':
            ser.write(b'T')  # Rotate Left
        elif key == 'e':
            ser.write(b'Y')  # Rotate Right
        elif key == 'z':
            ser.write(b'Q')  # Move Left Forward
        elif key == 'c':
            ser.write(b'E')  # Move Right Forward
        elif key == 'u':
            ser.write(b'Z')  # Move Left Backward
        elif key == 'o':
            ser.write(b'C')  # Move Right Backward
        elif key == 'x':
            ser.write(b'S')  # Stop
        elif key == 'i':
            ser.write(b'U')  # Servo1 Up
        elif key == 'k':
            ser.write(b'D')  # Servo1 Down
        elif key == 'j':
            ser.write(b'I')  # Servo2 Up
        elif key == 'l':
            ser.write(b'K')  # Servo2 Down
        elif key == 'm':
            ser.write(b'A')  # Activate Relay
        elif key == 'n':
            ser.write(b'V')  # Deactivate Relay
        elif key == 'q':
            ser.write(b'S')  # Stop before quitting
            running = False
            break

# ??? ???
cap = cv2.VideoCapture(0, cv2.CAP_V4L)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

running = True

# ? ?? ??? ??
key_thread = threading.Thread(target=handle_keys)
key_thread.start()

while running:
    # ??? ??? ??
    ret, video = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    video = cv2.flip(video, 1)
    cv2.imshow("image", video)

    # 'ESC' ?? ?? ??? ?? ?? ??
    if cv2.waitKey(1) & 0xFF == 27:  # ESC ?
        running = False
        break

# ?? ??
cap.release()
cv2.destroyAllWindows()
ser.close()
