
# UnMuted

Project UnMuted is a Sign Language Recognising app developed by team Clair_AI consisting of 10th-grade students from Delhi Public School Bangalore North Cambridge. The project aims to help people with hearing or speaking disabilities communicate with the world effectively.

## Deployment

To use the .py files download/clone Small_Dataset.

Create a folder called Sign Language Recognition

Open the folder in cmd and run the following command 
```bash
python -m venv sl
```
Then run this command to activate your virtual environment
```bash
.\sl\Scripts\activate
```
Move all the files downloaded earlier into the Sign Langauge Recognition folder

Before we use the project, the following things are needed:
    1. Mediapipe Package
    2. Tensorflow Package

To obtain the following packages run:
```cmd
python installation.py
```
To test if the device can detect your system camera the following needs to be run:
```cmd
python testing.py
```
If the program doesn't work, try changing 0 to 1 or 2 on line 6 in the testing.py file.

Once the initialization completes you can use the product. Run:
```cmd
python product.py
```
*Note:** The model has a chance of not working in your system. This issue of Tensorflow has been reported multiple times on the internet where a model doesn't work in another system. In that case, use train.py to train the model. Read the section on **Customization** to understand how to do it. If any problems occur please contact the number +91 81233 28682 (Nishanth Alampally).

## Customize

You can also train your model to create an application. First, use recorder.py to record your own signs. Each sign needs to be recorded 20 times. After recording a few signs use the train.py file to train the signs into a model. Before running train.py ensure you configure the model by changing the LSTM layers and LSTM units. Once the training reaches an accuracy of over 95% your model is ready. Then use the same configuration for the model in product.py as used in train.py and run the program to use your model. While running train.py take a look at Categorical_Accuracy to see how accurate the model is while training.

## Message From Developers

The project was made by three Grade 10 students - Kshipra Kashyap, Sai Juhith Paleti and Nishanth Alampally. The project is mainly based on the legacy version of the Mediapipe module developed by Google. The project will be updated as Mediapipe's new version is released in mid-2024. A GUI has also been made for the project but due to the incapability of Legacy Mediapipe's Holistic model and Tkinter, the GUI has not been implemented with the actual product. You can check out the GUI in the GUI folder.

## Future Plans

Clair_AI plans on continuing the project as soon as Mediapipe's new version is released. We plan to use ASLLVD and ASL-LEX - 2 large databases consisting of all signs in ASL to complete our project's first version. 
