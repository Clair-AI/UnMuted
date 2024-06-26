# Program to use the recorded signs to produce a Tensorflow Sequential model

import numpy as np
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard

folder_name = input("Name of folder where signs are stored? ")
DATA_PATH = os.path.join('{}'.format(folder_name)) 
actions = np.array(os.listdir(DATA_PATH))
no_sequences = 20
sequence_length = 30

# Obtaining the saved keypoints

label_map = {label:num for num, label in enumerate(actions)}
sequences, labels = [], []
for action in actions:
    for sequence in range(no_sequences):
        window = []
        for frame_num in range(sequence_length):
            res = np.load(os.path.join(DATA_PATH, action, str(sequence), "{}.npy".format(frame_num)))
            window.append(res)
        sequences.append(window)
        labels.append(label_map[action])

# Creating test data 

X = np.array(sequences)
y = to_categorical(labels).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05) 
log_dir = os.path.join('Logs')
tb_callback = TensorBoard(log_dir=log_dir)

# Creating and fitting the model
# Use relu or sigmoid activation

model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(30,126)))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))

model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy']) # Use Adam or Adamax optimizer
model.fit(X_train, y_train, epochs=1000, callbacks=[tb_callback]) # Try changing number of epochs if model reaches required accuracy quickly

model_name = input("What would you like to name your model? ")
model.save('{}.keras'.format(model_name))
