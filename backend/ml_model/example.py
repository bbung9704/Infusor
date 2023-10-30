
# TFLite for image segmentation model

import tensorflow as tf
import cv2
import numpy as np
import matplotlib.pyplot as plt

model = tf.lite.Interpreter(model_path="model.tflite")
# classes = [  "bg" ,  "infusor" ,  ]


# Learn about its input and output details
input_details = model.get_input_details()
output_details = model.get_output_details()

model.resize_tensor_input(input_details[0]['index'], (1, 256, 256, 3))
model.allocate_tensors()


img = cv2.imread('image.jpg')
img = cv2.resize(img, dsize=(256, 256))
img_np = np.array(img)[None].astype('float32')

model.set_tensor(input_details[0]['index'], img_np)
model.invoke()

output = model.get_tensor(output_details[0]['index'])[0].argmax(-1)
output = np.repeat(output[:,:,np.newaxis],3,-1)
output = np.array(output, np.uint8) * 255
output = cv2.resize(output, dsize=(360, 720))
cv2.imshow('', output)
cv2.waitKey()
cv2.destroyAllWindows()