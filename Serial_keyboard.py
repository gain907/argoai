import serial
import time
import sys
import tty
import termios
import cv2

# ??? ?? ?? (????? ??? ??? ??)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # ???? ???? ?? ?? ??

print("Use the following keys to control the RC car and servo motors:")
print("w: Move Forward, s: Move Backward, a: Move Left, d: Move Right")
print("q: Rotate Left, e: Rotate Right, z: Move Left Forward, c: Move Right Forward")
print("u: Move Left Backward, o: Move Right Backward, x: Stop")
print("i: Servo1 Up, k: Servo1 Down, j: Servo2 Up, l: Servo2 Down")
print("m: Activate Relay, n: Deactivate Relay")
print("Press 'q' to quit.")

# ??? ???
cap = cv2.VideoCapture(0, cv2.CAP_V4L)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

while True:
    # ??? ??? ??
    ret, video = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    video = cv2.flip(video, 1)
    cv2.imshow("image", video)

    # ??? ?? ??
    key = cv2.waitKey(30) & 0xFF
    if key == 27:  # ESC ?? ??? ??
        break
    elif key == ord('w'):
        ser.write(b'F')  # Forward
    elif key == ord('s'):
        ser.write(b'B')  # Backward
    elif key == ord('a'):
        ser.write(b'L')  # Move Left
    elif key == ord('d'):
        ser.write(b'R')  # Move Right
    elif key == ord('q'):
        ser.write(b'T')  # Rotate Left
    elif key == ord('e'):
        ser.write(b'Y')  # Rotate Right
    elif key == ord('z'):
        ser.write(b'Q')  # Move Left Forward
    elif key == ord('c'):
        ser.write(b'E')  # Move Right Forward
    elif key == ord('u'):
        ser.write(b'Z')  # Move Left Backward
    elif key == ord('o'):
        ser.write(b'C')  # Move Right Backward
    elif key == ord('x'):
        ser.write(b'S')  # Stop
    elif key == ord('i'):
        ser.write(b'U')  # Servo1 Up
    elif key == ord('k'):
        ser.write(b'D')  # Servo1 Down
    elif key == ord('j'):
        ser.write(b'I')  # Servo2 Up
    elif key == ord('l'):
        ser.write(b'K')  # Servo2 Down
    elif key == ord('m'):
        ser.write(b'A')  # Activate Relay
    elif key == ord('n'):
        ser.write(b'V')  # Deactivate Relay
    elif key == ord('q'):
        ser.write(b'S')  # Stop before quitting
        break

# ?? ??
cap.release()
cv2.destroyAllWindows()
ser.close()
