import numpy as np
import tensorflow as tf
import cv2
import serial
import time
import pandas as pd

# CNN 모델 불러오기
model_path = '/content/drive/MyDrive/Honam_Project/cnn_model.h5'
model = tf.keras.models.load_model(model_path)

# 시리얼 통신 설정
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # Arduino 초기화 시간 대기

# 클래스 레이블 설정
label_dict = {0:'B', 1:'F', 2:'L', 3:'R', 4:'S'}
# CSV 파일 경로
csv_path = '/content/drive/MyDrive/Honam_Project/dataset.csv'

# 이미지 전처리 함수
def preprocess_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"이미지를 로드할 수 없습니다: {image_path}")

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 경계선 감지
    edges = cv2.Canny(gray_image, threshold1=50, threshold2=150)
    
    # 이진화
    _, binary_image = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY)
    
    resized = cv2.resize(binary_image, (224, 224))
    normalized = resized / 255.0
    reshaped = np.reshape(normalized, (1, 224, 224, 1))
    return reshaped

# CSV 파일 로드 및 이미지와 레이블 매핑
data = pd.read_csv(csv_path, names=['timestamp', 'image_path', 'command'])
images = []
labels = []

for index, row in data.iterrows():
    image_path = row['image_path']
    label = row['command']
    try:
        image = preprocess_image(image_path)
        images.append(image)
        labels.append(label)
    except ValueError as e:
        print(e)

images = np.array(images)
labels = np.array(labels)

# 웹캠 초기화
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 224)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 224)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        preprocessed = preprocess_image(frame)
        prediction = model.predict(preprocessed)
        class_index = np.argmax(prediction, axis=1)[0]
        command = label_dict[class_index]

        # 시리얼로 명령 전송
        ser.write(command.encode())
        print(f"Sent command: {command}")

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC 키
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    ser.close()
