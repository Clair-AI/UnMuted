# Program to check whether system camera is being detected by the program

import cv2
from custom_funcs import mediapipe_detection
from custom_funcs import  draw_landmarks
from custom_funcs import mp_holistic 

# If the prgram doesn't work try changing 0 to other numbers like 1, 2 and so on....
cap = cv2.VideoCapture(0)
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        image, results = mediapipe_detection(frame, holistic)
        draw_landmarks(image, results)
        cv2.imshow('OpenCV Feed', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
