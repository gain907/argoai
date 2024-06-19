import numpy as np
import pandas as pd
import matplotlib as plt
import cv2



cap = cv2.VideoCapture(0,cv2.CAP_V4L)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)


while True:
    ret,video = cap.read()
    video = cv2.flip(video,1)    
    cv2.imshow("image", video)
    
    
    key = cv2.waitKey(30) & 0xFF
    if key == 27:
        break
    
cap.release()
cv2.destoryAllWindows()