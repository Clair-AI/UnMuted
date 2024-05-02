# Program to record signs and store as numpy arrays

import cv2
import numpy as np
import os
from custom_funcs import extract_keypoints
from custom_funcs import mediapipe_detection
from custom_funcs import  draw_landmarks
from custom_funcs import mp_holistic


# Infinite loop allowing user to take breaks after recording specified actions
while True:

    folder_name = input("What would you like to call the folder to save the signs in? ")
    DATA_PATH = os.path.join('{}'.format(folder_name)) 
    actions = input(r"Enter your signs (seperate with ', '): ").split(", ")
    actions = np.array(actions)
    no_sequences = 20
    sequence_length = 30
    
    # Creating files for each sign
    for action in actions: 
        for sequence in range(no_sequences):
            try: 
                os.makedirs(os.path.join(DATA_PATH, action, str(sequence)))
            except:
                pass
    
    cap = cv2.VideoCapture(0)
    
    # Using Legacy Mediapipe's Holistic Solution
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        for action in actions:
            for sequence in range(no_sequences):
                for frame_num in range(sequence_length):

                    ret, frame = cap.read()

                    # Converting the frame recorded into a mediapipe usable image
                    image, results = mediapipe_detection(frame, holistic)

                    draw_landmarks(image, results)
                    
                    if frame_num == 0: 
                        cv2.putText(image, 'STARTING COLLECTION', (120,200), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255, 0), 4, cv2.LINE_AA)
                        cv2.putText(image, 'Collecting frames for {} Video Number {}'.format(action, sequence), (15,12), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1, cv2.LINE_AA)
                        cv2.imshow('OpenCV Feed', image)
                        cv2.waitKey(2000)
                    else: 
                        cv2.putText(image, 'Collecting frames for {} Video Number {}'.format(action, sequence), (15,12), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1, cv2.LINE_AA)
                        cv2.imshow('OpenCV Feed', image)
                    
                    # Extracting and saving keypoints of both hands
                    keypoints = extract_keypoints(results)
                    npy_path = os.path.join(DATA_PATH, action, str(sequence), str(frame_num))
                    np.save(npy_path, keypoints)

                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break
                        
        cap.release()
        cv2.destroyAllWindows()
