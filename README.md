# 462ModelPipeline
462ModelPipeline

Welcome to the 462ModelPipeline! As an editor, please use the following instructions using conda:

- clone the github repo
- make sure your conda version is above 4.12.0 (23.1.0 works also)
- create a new conda environment using: ```conda create -n my_env python=3.9.12 ```
- install packages using ```pip install requirements.txt```


To run pyqt5 designer to create new UI designs, run ```pyqt5-tools designer```
To convert the resulting .ui file to python, run ```pyuic5 form.ui > form.py ```


To run the current protoype, run ```python3 display.py```

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




References
[1] J. Chen, Q. Ou, Z. Chi, and H. Fu, “Smile detection in the wild with deep convolutional neural networks,” Machine Vision and Applications, vol. 28, no. 1-2, pp. 173–183, 2016.

[2] "Estimation of continuous valence and arousal levels from faces in naturalistic conditions", Antoine Toisoul, Jean Kossaifi, Adrian Bulat, Georgios Tzimiropoulos and Maja Pantic, published in Nature Machine Intelligence, January 2021


