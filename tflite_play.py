import numpy as np
import cv2
import serial
import time
import tflite_runtime.interpreter as tflite

# TFLite 모델 로드
model_path = '/home/argo/myenv/cnn_model.tflite'
interpreter = tflite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# 입력 및 출력 텐서 정보 얻기
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# 시리얼 통신 설정
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # Arduino 초기화 시간 대기

# 클래스 레이블 설정
label_dict = {0:'B', 1:'F', 2:'L', 3:'R', 4:'S'}

# 웹캠 초기화
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 224)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 224)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

def preprocess_image(frame):
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 경계선 감지
    edges = cv2.Canny(gray_image, threshold1=50, threshold2=150)
    
    # 이진화
    _, binary_image = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY)
    
    resized = cv2.resize(binary_image, (224, 224))
    reshaped = np.reshape(resized, (1, 224, 224, 1)).astype(np.float32)
    return reshaped

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        preprocessed = preprocess_image(frame)
        
        # TFLite 모델 예측
        interpreter.set_tensor(input_details[0]['index'], preprocessed)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        
        class_index = np.argmax(output_data, axis=1)[0]
        # print(f"Predicted class: {class_index}")
        command = label_dict[class_index]

        # 시리얼로 명령 전송
        ser.write(command.encode())
        # print(f"Sent command: {command}")

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC 키
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    ser.close()