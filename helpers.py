#from mtcnn import MTCNN
from facenet_pytorch import MTCNN
from torchvision import transforms

import cv2
import cvlib as cv
import torch
import numpy as np

import pandas as pd
import numpy as np
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import ShortTermFeatures

class Preprocess():
    def __init__(self, prefix, count, images_path, processed_path):
        self.count = count
        self.prefix = prefix
        self.images_path = images_path
        self.processed_path = processed_path
        self.detector = MTCNN(keep_all=True, select_largest=True, post_process=False)

    def run(self):
        for i in range(1, self.count):
            img_path = self.images_path+self.prefix+f'{i}.jpg'
            image = cv2.imread(img_path)
            cropped_img = self.create_bounding_box(image) # method call
            try:
                cropped_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
            except: 
                cropped_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cropped_img = cv2.resize(cropped_img, (64, 64))
            cropped_img = (cropped_img - cropped_img.min()) / (cropped_img.max() - cropped_img.min()) * 255
            cropped_img = cropped_img.astype(np.uint8)
            gimage = cv2.equalizeHist(cropped_img)
            cv2.imwrite(self.processed_path + self.prefix + f"{i}.jpg", gimage)

    def crop(self, img,bbox):
        x_min, y_min, x_max, y_max = bbox[0], bbox[1],bbox[0] + bbox[2], bbox[1] + bbox[3]
        bbox_obj = img[y_min:y_max, x_min:x_max]
        return bbox_obj

    def create_bounding_box(self, image):

        faces = self.detector(image)
        
        if len(faces) < 1:
            #Use another detector here 
            face, confidences = cv.detect_face(image)
            chosen = confidences.index(max(confidences))
            bounding_box = face[chosen]
            cropped_image = self.crop(image, bounding_box[1])

        else:
            cropped_image = faces[0]
            cropped_image = cropped_image.permute(1, 2, 0).detach().cpu().numpy()


        return image, cropped_image

class VideoFrameData(torch.utils.data.Dataset):
    def __init__(self, prefix, count,  processed_path):
        self.prefix = prefix
        self.count = count 
        self.images_path = processed_path
        self.image_names = self._load_image_names()

    def _load_image_names(self):
        image_names = []
        for i in range(1, self.count):
            image_names.append(self.prefix+f"{i}.jpg")
        return image_names
    
    def __len__(self):
        return self.count-1
    
    def __getitem__(self, i):
        image_name= self.image_names[i]
        img_path = self.images_path + f'/{image_name}'
        image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        fimage = transforms.ToTensor()(image)
        return fimage

class AudioExtractFeatures():
    def __init__(self, audio_path):
        self.audio_path = audio_path

    def __compute_features__(signal, sampling_rate):
        """
        Mid-term feature extraction
        """
        mid_window = 1.0
        mid_step = 1.0
        short_window = 0.050
        short_step = 0.050

        short_features, short_feature_names = \
            ShortTermFeatures.feature_extraction(signal, sampling_rate,
                                                short_window, short_step)

        n_stats = 2
        n_feats = len(short_features)
        #mid_window_ratio = int(round(mid_window / short_step))
        mid_window_ratio = round((mid_window -
                                (short_window - short_step)) / short_step)
        mt_step_ratio = int(round(mid_step / short_step))

        mid_features, mid_feature_names = [], []
        for i in range(n_stats * n_feats):
            mid_features.append([])
            mid_feature_names.append("")

        # for each of the short-term features:
        for i in range(n_feats):
            cur_position = 0
            num_short_features = len(short_features[i])
            mid_feature_names[i] = short_feature_names[i] + "_" + "mean"
            mid_feature_names[i + n_feats] = short_feature_names[i] + "_" + "std"

            while cur_position < num_short_features:
                end = cur_position + mid_window_ratio
                if end > num_short_features:
                    end = num_short_features
                cur_st_feats = short_features[i][cur_position:end]

                mid_features[i].append(np.mean(cur_st_feats))
                mid_features[i + n_feats].append(np.std(cur_st_feats))
                cur_position += mt_step_ratio
        mid_features = np.array(mid_features)
        mid_features = np.nan_to_num(mid_features)
        return mid_features, short_features, mid_feature_names
    
    def __append_labels__(features_df):
        sample_score = 23
        score = sample_score

        # SEVERITY 1
        if score > 0 and score < 9:
            features_df["Diagnosis"] = 1
        # SEVERITY 2
        if score > 10 and score < 14:
            features_df["Diagnosis"] = 2
        # SEVERITY 3
        if score > 15 and score < 19:
            features_df["Diagnosis"] = 3
        # SEVERITY 4
        if score > 20 and score < 27:
            features_df["Diagnosis"] = 4

        # Save to csv
        csv_filename = "features_sample.csv"
        features_df.to_csv(csv_filename, index=False, mode="a")
