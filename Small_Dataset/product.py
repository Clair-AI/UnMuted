# Project UnMuted
# By team Clair_AI

import cv2
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import os
from custom_funcs import extract_keypoints
from custom_funcs import mediapipe_detection
from custom_funcs import  draw_landmarks
from custom_funcs import mp_holistic

DATA_PATH = os.path.join('MP_Data') 
actions = np.array(os.listdir(DATA_PATH))

# Loading the pre-trained sequential model

model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(30,126)))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

model_name = input("What is the name of the model (with extension)? ")
model.load_weights('{}'.format(model_name))

sequence = []
sentence = []
final_sentence = []
predictions = []
threshold = 0.95 # Change threshold to change the accuracy and latency

cap = cv2.VideoCapture(0)
temp = np.concatenate([np.zeros(21*3), np.zeros(21*3)])

frame_num = 0
a = 0
first_time = True
        
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()

        image, results = mediapipe_detection(frame, holistic)
        
        draw_landmarks(image, results)
        
        keypoints = extract_keypoints(results)
        if not (keypoints==temp).all():
            sequence.append(keypoints)
            sequence = sequence[-30:]
            if first_time == True:
                first_time = False
                a = frame_num+3
            else:
                if a + 3 < frame_num:
                    if (len(sequence) == 30):
                        res = model.predict(np.expand_dims(sequence, axis=0))[0]
                        predictions.append(np.argmax(res))
                        if (np.bincount(predictions[-11:]).argmax() == np.argmax(res)) and (len(predictions) > 7): # Experiment with -11 and 7 to manipulate latency and accuracy
                            if np.count_nonzero(np.array(predictions) == np.argmax(res)) > 6: # Experiment with 6 to change accuracy
                                if res[np.argmax(res)] > threshold: 
                                    if len(sentence) > 0: 
                                        if actions[np.argmax(res)] != sentence[-1]:
                                            sentence.append(actions[np.argmax(res)])
                                            final_sentence.append(actions[np.argmax(res)])
                                            predictions = []
                                            a = frame_num
                                    else:
                                        sentence.append(actions[np.argmax(res)])
                                        final_sentence.append(actions[np.argmax(res)])
                                        predictions = []
                                        a = frame_num
        
                        if len(sentence) > 5: 
                            sentence = sentence[-5:]


        cv2.rectangle(image, (0,0), (640, 40), (245, 117, 16), -1)
        cv2.putText(image, ' '.join(sentence), (3,30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('OpenCV Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

        frame_num += 1

    cap.release()
    cv2.destroyAllWindows()

print("Sentence:", " ".join(final_sentence))