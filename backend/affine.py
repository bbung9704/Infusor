import cv2, math, uuid
import numpy as np
from pyzbar.pyzbar import decode
from fastapi import HTTPException


class Transformer:
    def __init__(self, image):
        self._image = image
        self._height, self._width, self._channel = self._image.shape
        self.qrcode = decode(self._image) # Detect 안되면 qrcode = []
        self._points = None
        self._transPoints = None
        self._minAreaRect = None
        self._minAreaRectCenter = None
        self._minAreaRectAngle = None

        if self.qrcode:
            self._setPoints()
            self._setMinAreaRect()
            self._setTransPoints()
        
        else:
            raise HTTPException(status_code=400, detail='QRCode is not detected.')
        
    def Rotate(self, image):
        matrix = cv2.getRotationMatrix2D(center=self._minAreaRectCenter, angle=self._minAreaRectAngle, scale=1)
        result = cv2.warpAffine(image, matrix, (self._width, self._height)) 
        return result
    
    def Affine(self, image):
        matrix = cv2.getAffineTransform(np.array([self._points[0], self._points[1], self._points[3]]), np.array([self._transPoints[0], self._transPoints[1], self._transPoints[3]]))
        result = cv2.warpAffine(image, matrix, (self._width, self._height))
        return result

    def Perspective(self, image):
        matrix = cv2.getPerspectiveTransform(self._points, self._transPoints)
        result = cv2.warpPerspective(image, matrix, (self._width, self._height))
        return result
    
    def _setPoints(self):
        lt = self.qrcode[0].polygon[0]
        lb = self.qrcode[0].polygon[1]
        rb = self.qrcode[0].polygon[2]
        rt = self.qrcode[0].polygon[3]
        self._points = np.float32([[lt.x, lt.y], [lb.x, lb.y], [rb.x, rb.y], [rt.x, rt.y]])

    def _setMinAreaRect(self):
        self._minAreaRect = cv2.minAreaRect(self._points)
        self._minAreaRectCenter = self._minAreaRect[0]
        self._minAreaRectAngle = self._minAreaRect[2] if self._minAreaRect[2] < 45 else self._minAreaRect[2] - 90

    def _setTransPoints(self):
        # 변환할 box 위치
        trans_points = cv2.minAreaRect(self._points)
        trans_points = cv2.boxPoints(self._minAreaRect)

        # minAreaRect에 의한 boxPoint 방향이 제대로 안잡혀 생기는 trans_point 방향 문제 수정
        new_trans_points = [0, 0, 0, 0]
        fpoints = self._points.copy()
        for i in trans_points:
            short = math.sqrt(self._height^2 + self._width^2)
            id = 0
            for idx, j in enumerate(fpoints):
                d = self.__distance(i, j)
                if d < short:
                    short = d
                    id = idx
            new_trans_points[id] = i
            np.delete(fpoints, id, 0)

        trans_points = np.array(new_trans_points)
        self._transPoints = np.float32(trans_points)
    

    def __distance(self, target, input):
        result = math.sqrt( math.pow(target[0] - input[0], 2) + math.pow(target[1] - input[1], 2))
        return result

class ImageProcessor:
    def __init__(self, ratio=0.3):
        self.ratio = ratio

    def clientToServer(self, image):
        image = np.frombuffer(image, dtype = np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        image_decoded = cv2.resize(image, dsize=(0,0), fx=self.ratio, fy=self.ratio)

        return image_decoded

    def serverToClient(self, image):
        _, enc_image = cv2.imencode('.jpeg', image)
        image_bytes = enc_image.tobytes()

        return image_bytes




# def transform(img, option):
#     # QR Code 인식 안되는 경우, Exception
#     qrcode = decode(img)
#     if len(qrcode) == 0:
#         raise HTTPException(status_code=500, detail='QRCode is not detected.')

#     # QRCode Edge points & Image size
#     # *** Left-Top point부터 반시계 방향으로 point 표시
#     height, width, _ = img.shape

#     lt = qrcode[0].polygon[0]
#     lb = qrcode[0].polygon[1]
#     rb = qrcode[0].polygon[2]
#     rt = qrcode[0].polygon[3]
#     points = np.float32([[lt.x, lt.y], [lb.x, lb.y], [rb.x, rb.y], [rt.x, rt.y]])

#     # minAreaRect 탐색
#     trans_points = cv2.minAreaRect(points)
#     minArea = trans_points
#     trans_points = cv2.boxPoints(trans_points)

#     # minAreaRect에 의한 boxPoint 방향이 제대로 안잡혀 생기는 trans_point 방향 문제 수정
#     new_trans_points = [0, 0, 0, 0]
#     fpoints = points.copy()
#     for i in trans_points:
#         short = math.sqrt(height^2 + width^2)
#         id = 0
#         for idx, j in enumerate(fpoints):
#             d = distance(i, j)
#             if d < short:
#                 short = d
#                 id = idx
#         new_trans_points[id] = i
#         np.delete(fpoints, id, 0)

#     trans_points = np.array(new_trans_points)
#     trans_points = np.float32(trans_points)

#     # minAreaRect에 의한 angle이 특정각도 이상일 때, 90도 회전되는 문제 수정
#     # *** minAreaRect가 뭔지 이해X
#     if minArea[2] > 50:
#         list_minArea = list(minArea)
#         list_minArea[2] -= 90
#         minArea = tuple(list_minArea)
    
#     # Affine Transform, Perspective Transform and Rotation
#     match option:
#         case 'aff':
#             matrix = cv2.getAffineTransform(np.array([points[0], points[1], points[3]]), np.array([trans_points[0], trans_points[1], trans_points[3]]))
#             dst = cv2.warpAffine(img, matrix, (width, height))
#         case 'rot':
#             matrix = cv2.getRotationMatrix2D(center=minArea[0], angle=minArea[2], scale=1)
#             dst = cv2.warpAffine(img, matrix, (width, height))    
#         case 'per':
#             matrix = cv2.getPerspectiveTransform(points, trans_points)
#             dst = cv2.warpPerspective(img, matrix, (width, height))

#     return dst

# # 이미지 전처리
# def image_process(dst):
#     _, enc_image = cv2.imencode('.jpeg', dst)
#     image_bytes = enc_image.tobytes()

#     return image_bytes

# # 거리 계산
# def distance(target, input):
#     result = math.sqrt( math.pow(target[0] - input[0], 2) + math.pow(target[1] - input[1], 2))
#     return result