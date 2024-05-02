# Program to install all packages required to run project UnMuted

import os

dependencies = {"tensorflow":"tensorflow", "cv2":"opencv-python", "numpy":"numpy", "mediapipe":"mediapipe", "matplotlib":"matplotlib", "sklearn":"scikit-learn"}

for i in dependencies:
    try:
        import i
    except ModuleNotFoundError:
        a = dependenices[i]
        os.system(f"pip install {a}")
