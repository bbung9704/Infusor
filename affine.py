import cv2, math, base64, uuid
import numpy as np
from pyzbar.pyzbar import decode
from fastapi import HTTPException


class Transformer:
    def __init__(self, image):
        self._image = image
        self.file_name = str(uuid.uuid1())
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
            # image = processor.serverToClient(self._image)
            # blob = bucket.blob('fail/'+ self.file_name + '.jpeg')
            # blob.upload_from_string(image, content_type='image/jpeg')
            raise HTTPException(status_code=400, detail='QR코드를 인식할 수 없습니다.')
        
    def reset(self, image):
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
            # image = processor.serverToClient(self._image)
            # blob = bucket.blob('fail/'+ self.file_name + '.jpeg')
            # blob.upload_from_string(image, content_type='image/jpeg')
            raise HTTPException(status_code=400, detail='QR코드를 인식할 수 없습니다.')
        
    def drawPoint(self, image):
        alpha = 0.7
        image_copy = image.copy()
        for idx, p in enumerate(self._points):
            p = np.int32(p)
            if idx == 0:
                first = p
                start = p
            if idx == 3:
                end, start = start, p
                cv2.line(image, start, end, color=(0,0,255), thickness=3)
                end, start = start, first
                cv2.line(image, start, end, color=(0,0,255), thickness=3)
            else:
                end, start = start, p
                cv2.line(image, start, end, color=(0,0,255), thickness=3)

        image = cv2.addWeighted(image, alpha, image_copy, 1-alpha, 0)

        return image
    
    def drawTransPoint(self, image):
        alpha = 0.7
        image_copy = image.copy()
        for idx, p in enumerate(self._transPoints):
            p = np.int32(p)
            if idx == 0:
                first = p
                start = p
            if idx == 3:
                end, start = start, p
                cv2.line(image, start, end, color=(0,255,0), thickness=3)
                end, start = start, first
                cv2.line(image, start, end, color=(0,255,0), thickness=3)
            else:
                end, start = start, p
                cv2.line(image, start, end, color=(0,255,0), thickness=3)

        image = cv2.addWeighted(image, alpha, image_copy, 1-alpha, 0)

        return image
    
    def MoveQrToCenter(self, image):
        dx = self._width/2 - self._minAreaRectCenter[0]
        dy = self._height/2 - self._minAreaRectCenter[1]
        matrix = np.float32([[1,0,dx], [0,1,dy]])
        result = cv2.warpAffine(image, matrix, (self._width, self._height))

        return result
        
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
    
    def MakeConstantQr(self, image):
        base_size = (self._width, self._height, 3)
        base = np.zeros(base_size, np.uint8)
        target_length = 100.
        width = self.qrcode[0].rect.width
        height = self.qrcode[0].rect.height

        if width < target_length or height < target_length:
            raise HTTPException(status_code=400, detail='QR코드가 너무 멀리 있습니다.')

        fx = target_length / width
        fy = target_length / height
        resized_img = cv2.resize(image, dsize=(0,0), fx=fx, fy=fy)

        base[int(base_size[1]/2 - resized_img.shape[0]/2) : int(base_size[1]/2 + resized_img.shape[0]/2), 
             int(base_size[0]/2 - resized_img.shape[1]/2) : int(base_size[0]/2 + resized_img.shape[1]/2)] = resized_img
        return base
    
    def CropInfusor(self, image):
        result = image[np.int32(self._height * 2/8) : np.int32(self._height * 6/8), 
                np.int32(self._width * 3/8) : np.int32(self._width * 5/8)]
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
        trans_points = cv2.boxPoints(self._minAreaRect)

        # minAreaRect에 의한 boxPoint 방향이 제대로 안잡혀 생기는 trans_point 방향 문제 수정
        new_trans_points = [0, 0, 0, 0]
        fpoints = self._points.copy()
        for i in trans_points:
            # short = math.sqrt(self._height^2 + self._width^2)
            short = 10**5
            id = 0
            for idx, j in enumerate(fpoints):
                d = self.__distance(i, j)
                if d <= short:
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

    def clientToServerBase64(self, image):
        image = base64.b64decode(image)
        image = np.fromstring(image, dtype = np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        image_decoded = cv2.resize(image, dsize=(0,0), fx=self.ratio, fy=self.ratio)

        return image_decoded

    def serverToClient(self, image):
        _, enc_image = cv2.imencode('.jpeg', image)
        image_bytes = enc_image.tobytes()

        return image_bytes
    
processor = ImageProcessor(1)