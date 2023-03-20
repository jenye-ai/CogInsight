#from mtcnn import MTCNN
from facenet_pytorch import MTCNN
from torchvision import transforms

import cv2
import cvlib as cv
import torch
import numpy as np

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