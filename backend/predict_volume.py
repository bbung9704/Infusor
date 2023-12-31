import cv2, os
import numpy as np

def cal_iou(tgt_np, compare):
    overlap = tgt_np * compare
    union = tgt_np + compare
    iou = overlap.sum()/float(union.sum())
    return iou

# def predict_volume(tgt):
#     result = [0 for _ in range(23)]
#     cnt = [0 for _ in range(23)]

#     tgt_np = np.array(tgt, dtype=bool)

#     root = 'images/label'
#     labels = os.listdir(root)
#     for label in labels:
#         file_name = label.split('.')[0]
#         volume = file_name.split('_')[-1]
#         idx = int(int(volume) / 10)

#         img = cv2.imread(root + '/' + label)
#         compare = np.array(img, dtype=bool)
#         iou = cal_iou(tgt_np, compare)

#         cnt[idx] += 1
#         result[idx] += iou

#     for i in range(len(result)):
#         result[i] /= cnt[i]

#     max_iou = max(result)
#     predict = result.index(max_iou) * 10

#     return predict

def predict_volume(tgt):
    tgt = np.array(tgt) / 255
    tgt_area = np.sum(tgt) * 3
    coef = 0.0007725
    intercept = -42.33394674384486
    predict = round(coef * tgt_area + intercept)

    if predict > 220: predict = 220
    elif predict < 0: predict = 0

    return predict