# CogInsight
Monitoring Therapeutic Progress for Depressive Symptoms

Authors: Jennifer Ye, Catherine Bui, Kayley Ting, Katie Chen

Capstone Project Advisor: Dr. Paul Fieguth

![alt text](https://github.com/jenye-ai/CogInsight/demo.gif](https://github.com/jenye-ai/CogInsight/blob/a3_symposium/demo.gif)

Solution to be used by young adults aged 18-23 engaging in CBT to improve objectivity in the longitudinal monitoring of depressive symptoms, empowering users and clinicians with objective data points helping improve mental health outcomes by providing quantitative and interpretable metrics of psychological indicators without being intrusive.

# Features
- **Objective Monitoring:** Provides objective data points to monitor depressive symptoms over time.
- **Quantitative Metrics:** Offers interpretable metrics of psychological indicators backed by literature.
- **Non-Intrusive Data Collection:** Gathers data without being overly burdensome to users, capturing involuntary movements and data that are hard for users to manipulate.
- **Multimodal Data Collection:** Utilizes audio, video, and interactive modalities to capture a comprehensive picture of patients' mental health, enabling a holistic understanding of their mental and emotional well-being.
- **Visualizations and Reports:** Presents data through clear visual aids and informative reports.

# Setup

Welcome to the CogInsight! As an editor, please use the following instructions using conda:

- clone the github repo
- make sure your conda version is above 4.12.0 (23.1.0 works also)
- create a new conda environment using: ```conda create -n my_env python=3.9.12 ```
- install packages using ```pip install requirements.txt```


To run pyqt5 designer to create new UI designs, run ```pyqt5-tools designer```
To convert the resulting .ui file to python, run ```pyuic5 form.ui > form.py ```

To run the current protoype, run ```python3 GUI.py```

Make sure that in constants.py, the name of the file you save to record you video is the same as the VIDEO_PATH variable. 
Make sure to also specify your OS type. (Mac vs Windows)

Also make sure that your output dir matches the constant file OUTPUT_DIR variable

## constants.py
Contains all the modifiable variables in the program. Includes paths to data and results, as well as OS type.

## display.py
Contains all the PyQt5 methods and classes used to design the UI.

## helpers.py 
Contains all the data preprocessing steps/modified data loaders.

## model.py 
Contains all the models in the pipeline. Models are currently all written in PyTorch.
Current models:
- Modified implementation of SmileCNN [1]
- Emonet [2]

## pipeline.py
Takes in video path link, preprocesses the data using functions in helpers.py and sends them to the models in model.py. Returns all the metrics obtainined from data using models.


# References
[1] J. Chen, Q. Ou, Z. Chi, and H. Fu, “Smile detection in the wild with deep convolutional neural networks,” Machine Vision and Applications, vol. 28, no. 1-2, pp. 173–183, 2016.

[2] "Estimation of continuous valence and arousal levels from faces in naturalistic conditions", Antoine Toisoul, Jean Kossaifi, Adrian Bulat, Georgios Tzimiropoulos and Maja Pantic, published in Nature Machine Intelligence, January 2021


