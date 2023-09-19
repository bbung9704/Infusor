import cv2, os
import numpy as np
from affine import Transformer

ratio = 1
root = "images/"
files = os.listdir("images/")

for file in files:
    img_dir = root + file
    img = cv2.imread(img_dir, cv2.IMREAD_COLOR)
    transformer = Transformer(img)

    centered = transformer.MoveQrToCenter(transformer._image)
    aff = transformer.Perspective(centered)
    affrot = transformer.Rotate(aff)

    transformer.reset(affrot)
    constant = transformer.MakeConstantQr(affrot)

    crop = transformer.CropInfusor(constant)

    cv2.imshow('image', crop)
    cv2.waitKey()

cv2.destroyAllWindows()