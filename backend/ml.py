from keras_segmentation.models.unet import vgg_unet
import tensorflow as tf
import numpy as np


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
        self.model = vgg_unet(n_classes=2 ,  input_height=736, input_width=384)
        self.model.load_weights('ckp/test')
    
    def getPrediction(self, img_root):
        out = self.model.predict_segmentation(
            inp = img_root,
            out_fname="images/out.png"
        )
        # 0~255로 변환
        out = np.array(out, dtype=np.uint8)
        out = np.repeat(out[:,:,np.newaxis],3,-1)
        out *= 255
        
        return out
