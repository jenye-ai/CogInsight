import cv2
import constants
import collections
import numpy as np
import os
import torch
import pickle

import pandas as pd
import numpy as np
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import ShortTermFeatures

from torch.utils.data import DataLoader
from helpers import Preprocess, VideoFrameData, AudioExtractFeatures
from models import SmileCNNSVM, EmotionDetector
from pytorch_tabnet.tab_model import TabNetClassifier

EXPRESSIONS = {0: 'neutral', 1:'happy', 2:'sad', 3:'surprise', 4:'fear', 5:'disgust', 6:'anger', 7:'contempt', 8:'none'}

class VideoPipeline():
    def __init__(self, dir, frameRate=0.5, prefix = "image", folder = "original_frames", processed_folder = "processed_frames"):
        self.frameRate = frameRate
        self.frame_path = dir+ folder + "/" 
        self.processed_path = dir+ processed_folder + "/" 
        self.prefix = prefix
        self.final_count = None
        self.num_smiles = 0
        self.time_smiling = 0
        self.valence = []
        self.arousal = []
        self.emotion = []

        pass
        
    def execute(self, video_path):

        #Step 0 convert video to images
        print("Creating Folders ...")
        if not os.path.exists(self.frame_path):
            os.mkdir(self.frame_path)
        if not os.path.exists(self.processed_path):
            os.mkdir(self.processed_path)
        print("Converting Video to Frames ...")
        images = self._convertToFrames(video_path)

        #Step 1 crop images
        print("Processing frames for SmileCNN ...")
        preprocessor = Preprocess(prefix=self.prefix, count=self.final_count, images_path=self.frame_path, processed_path = self.processed_path)
        preprocessor.run()

        #Step 2 smile classifier
        print("Running SmileCNN ...")
        #Load the feature extractor
        model = SmileCNNSVM()
        model.load_state_dict(torch.load(constants.SMILECNN_PATH, map_location=torch.device('cpu')))
        model.eval()
        dataset = VideoFrameData(self.prefix, self.final_count,  self.processed_path)
        data_loader = DataLoader(dataset, batch_size=len(dataset), shuffle=False)

        print(f"Generating Features for the training set using the SmileCNN")
        with torch.no_grad():
            for x in data_loader:
                yhat, svm_features = model(x)
        print("Feature Generation Complete!")

        print("Detecting Smiles ...")
        SVM_model = pickle.load(open(constants.SVM_PATH, 'rb'))
        smiles = SVM_model.predict(svm_features)

        print("Calculating Time Smiling ...")
        self.time_smiling = collections.Counter(smiles)[1]*self.frameRate

        print("Calculating Number of Smiles ...")
        prev = 0
        for i in smiles:
            if prev==0 and i==1:
                self.num_smiles += 1
                prev = 1
            elif i==0:
                prev = 0
        
        print("Calculating Emotions, Valence, and Arousal ...")
        #step 3 valence and arousal
        emonet = EmotionDetector(constants.EMONET_PATH)
        for i in images[:-1]:
            expression, valence, arousal = emonet.execute(i)
            self.valence.append(valence)
            self.arousal.append(arousal)
            self.emotion.append(expression)
        print("Finish!")
        return {"num_smiles": self.num_smiles,
                "time_smiling": self.time_smiling,
                "valence": np.squeeze(np.array([t.numpy() for t in self.valence]).astype(float)),
                "arousal": np.squeeze(np.array([t.numpy() for t in self.arousal]).astype(float)),
                "emotion": self.emotion,
                "frames": len(self.emotion),
                "time": len(self.emotion)*self.frameRate}
        
    def _convertToFrames(self, file_path):
        video = cv2.VideoCapture(file_path)
        sec = 0
        count=1
        images = []
        success, image = self.getFrame(video, sec, count)
        images.append(image)
        while success:
            count = count + 1
            sec = sec + self.frameRate
            sec = round(sec, 2)
            success, image = self.getFrame(video, sec, count)
            images.append(image)
        self.final_count = count
        return images

    def getFrame(self, videoframe, sec, count):
        videoframe.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
        hasFrames,image = videoframe.read()
        if hasFrames:
            path = self.frame_path + self.prefix+str(count)+".jpg"
            cv2.imwrite(path, image)     # save frame as JPG file
        return hasFrames, image
    
class AudioPipeline():
    def __init__(self, dir, frameRate=0.5, prefix = "image", folder = "original_frames", processed_folder = "processed_frames"):
        self.frameRate = frameRate
        self.frame_path = dir+ folder + "/" 
        self.processed_path = dir+ processed_folder + "/" 
        self.valence = []

        pass 

    def execute(self, video_path):

        #Step 0 load audio file
        wav_file = constants.DEMO_AUDIO
        sampling_rate, signal = audioBasicIO.read_audio_file(wav_file)
        signal = audioBasicIO.stereo_to_mono(signal)

        #Step 1 run feature extraction
        feature_extractor = AudioExtractFeatures(wav_file)
        mid_features, short_features, feature_names = feature_extractor.__compute_features__(signal, sampling_rate)
        mid_features = np.transpose(mid_features)
        features_df = pd.DataFrame(mid_features,
                        columns=feature_names)
        
        #Step 2 append labels and writes to csv
        feature_extractor.__append_labels__(features_df)

        #Step 3 (TODO: process actual wav file not just sample)
        audio_filename = constants.AUDIO_PATH
        model = TabNetClassifier()
        model.load_model(audio_filename)

        
