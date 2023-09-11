import cv2, math
import numpy as np
from pyzbar.pyzbar import decode
from fastapi import HTTPException
    

def transform(img, option):
    qrcode = decode(img)
    if len(qrcode) == 0:
        raise HTTPException(status_code=500, detail='QRCode is not detected.')

    height, width, _ = img.shape

    lt = qrcode[0].polygon[0]
    lb = qrcode[0].polygon[1]
    rb = qrcode[0].polygon[2]
    rt = qrcode[0].polygon[3]

    points = np.float32([[lt.x, lt.y], [lb.x, lb.y], [rb.x, rb.y], [rt.x, rt.y]])

    trans_points = cv2.minAreaRect(points)
    minArea = trans_points
    trans_points = cv2.boxPoints(trans_points)

    new_trans_points = [0, 0, 0, 0]
    fpoints = points.copy()

    for i in trans_points:
        short = math.sqrt(height^2 + width^2)
        id = 0
        for idx, j in enumerate(fpoints):
            d = distance(i, j)
            if d < short:
                short = d
                id = idx
        new_trans_points[id] = i
        np.delete(fpoints, id, 0)

    trans_points = np.array(new_trans_points)
    trans_points = np.float32(trans_points)

    if minArea[2] > 50:
        list_minArea = list(minArea)
        list_minArea[2] -= 90
        minArea = tuple(list_minArea)
        
    match option:
        case 'aff':
            matrix = cv2.getAffineTransform(np.array([points[0], points[1], points[3]]), np.array([trans_points[0], trans_points[1], trans_points[3]]))
            dst = cv2.warpAffine(img, matrix, (width, height))
        case 'rot':
            matrix = cv2.getRotationMatrix2D(center=minArea[0], angle=minArea[2], scale=1)
            dst = cv2.warpAffine(img, matrix, (width, height))    
        case 'per':
            matrix = cv2.getPerspectiveTransform(points, trans_points)
            dst = cv2.warpPerspective(img, matrix, (width, height))

    return dst
    
def image_process(dst):
    _, enc_image = cv2.imencode('.jpeg', dst)
    image_bytes = enc_image.tobytes()

    return image_bytes

def distance(target, input):
    result = math.sqrt( math.pow(target[0] - input[0], 2) + math.pow(target[1] - input[1], 2))
    return result