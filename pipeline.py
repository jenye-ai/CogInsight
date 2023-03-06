import cv2
import constants
import os
import torch
import pickle

from torch.utils.data import DataLoader
from helpers import Preprocess, VideoFrameData
from models import SmileCNNSVM

class VideoPipeline():
    def __init__(self, dir, frameRate=0.5, prefix = "image", folder = "original_frames", processed_folder = "processed_frames"):
        self.frameRate = frameRate
        self.frame_path = dir+ folder + "/" 
        self.processed_path = dir+ processed_folder + "/" 
        self.prefix = prefix
        self.final_count = None
        self.num_smiles = 0
        self.time_smiling = 0

        pass
        
    def execute(self, video_path):

        #Step 0 convert video to images
        print("Creating Folders ...")
        if not os.path.exists(self.frame_path):
            os.mkdir(self.frame_path)
        if not os.path.exists(self.processed_path):
            os.mkdir(self.processed_path)
        print("Converting Video to Frames ...")
        self._convertToFrames(video_path)

        #Step 1 crop images
        print("Processing frames for SmileCNN ...")
        preprocessor = Preprocess(prefix=self.prefix, count=self.final_count, images_path=self.frame_path, processed_path = self.processed_path)
        preprocessor.run()

        #Step 2 smile classifier
        print("Running SmileCNN ...")
        #Load the feature extractor
        model = SmileCNNSVM()
        model.load_state_dict(torch.load(constants.SMILECNN_PATH))
        model.eval()
        dataset = VideoFrameData(self.prefix, self.final_count,  self.processed_path)
        data_loader = DataLoader(dataset, batch_size=len(dataset), shuffle=False)

        print(f"Generating Features for the training set using the SmileCNN")
        with torch.no_grad():
            for x in data_loader:
                yhat, svm_features = model(x)
        print("Feature Generation Complete!")


        SVM_model = pickle.load(open(constants.SVM_PATH, 'rb'))
        smiles = SVM_model.predict(svm_features)
        self.time_smiling = smiles.count(1)*self.frameRate
        #get number of times smiled 


        #for i in smiles:


        #step 3 valence and arousal

        #Load Video and save into frames
        pass
        
    def _convertToFrames(self, file_path):
        video = cv2.VideoCapture(file_path)
        sec = 0
        count=1
        success = self.getFrame(video, sec, count)
        while success:
            count = count + 1
            sec = sec + self.frameRate
            sec = round(sec, 2)
            success = self.getFrame(video, sec, count)
        self.final_count = count

    def getFrame(self, videoframe, sec, count):
        videoframe.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
        hasFrames,image = videoframe.read()
        if hasFrames:
            path = self.frame_path + self.prefix+str(count)+".jpg"
            cv2.imwrite(path, image)     # save frame as JPG file
        return hasFrames
