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
class ML_Model:
    def __init__(self):
        ## tf
        self.input_shape = (736, 384, 3)
        self.model = DeepLabV3Plus(self.input_shape, num_classes=1)
        self.model.load_weights("ckp/DeepLabV3Plus_60.h5")

    def output2binary(self, imgs):
        img = imgs[0]
        img = np.array(img)
        img[img >= 0.5] = 1
        img[img < 0.5] = 0
        img = np.repeat(img, 3, -1)
        img = np.array(img, np.uint8)
        return img

    def binary2color(self,img):
        img *= 255
        return img

    def getPrediction(self, img_root):
        ## tf
        img = cv2.resize(img_root, dsize=(384, 736))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        img = ((img / 255) ** 1.5) * 255        # 감마 보정 -> 모델 정확도 높히기 위해 인풋 이미지의 contrast 높임.
        img = np.array(img[np.newaxis, :, :])

        out = self.model(img)
        out = self.output2binary(out)

        return out
