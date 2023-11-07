import tensorflow as tf
import numpy as np
import cv2
from ml_model.deeplabv3plus import DeepLabV3Plus

def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@singleton
class Unet:
    def __init__(self):
        ## tf
        self.input_shape = (736, 384, 3)
        self.model = DeepLabV3Plus(self.input_shape, num_classes=1)
        self.model.load_weights("ckp/DeepLabV3Plus_75_try9.h5")

    def output2image(self, imgs):
        img = imgs[0]
        img = np.array(img)
        img[img >= 0.5] = 1
        img[img < 0.5] = 0
        img *= 255
        img = np.repeat(img, 3, -1)
        img = np.array(img, np.uint8)
        return img

    def getPrediction(self, img_root):
        ## tf
        img = cv2.resize(img_root, dsize=(384, 736))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        img = ((img / 255) ** 1.5) * 255        # 감마 보정
        img = np.array(img[np.newaxis, :, :])

        out = self.model(img)
        out = self.output2image(out)
        ##

        # out = self.model.predict_segmentation(
        #     inp = img_root,
        #     out_fname="images/out.png"
        # )
        # # 0~255로 변환
        # out = np.array(out, dtype=np.uint8)
        # out = np.repeat(out[:,:,np.newaxis],3,-1)
        # out *= 255
        
        return out
