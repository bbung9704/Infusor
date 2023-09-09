import cv2
import numpy as np

# im = cv2.imread("test3.jpeg")
# height, width, channel = im.shape

# det = cv2.QRCodeDetector()
# (rv, points) = det.detect(im)

# points = np.float32(points[0])
# points_int = np.int_(points)

# trans_points = cv2.minAreaRect(points)
# trans_points = cv2.boxPoints(trans_points)

# trans_points = np.array([trans_points[1], trans_points[2], trans_points[3], trans_points[0]])

# trans_points = np.float32(trans_points)
# trans_points_int = np.int_(trans_points)

# matrix = cv2.getPerspectiveTransform(points, trans_points)
# dst = cv2.warpPerspective(im, matrix, (width, height))
# dst = cv2.resize(dst, dsize=None, fx=0.15, fy=0.15)
# im = cv2.resize(im, dsize=None, fx=0.15, fy=0.15)

# result = cv2.hconcat([im, dst])
# cv2.imshow("larger", result)
# cv2.waitKey()


class QRCodeDetection(Exception):
    def __str__(self):
        return "QRCode가 인식되지 않습니다."

def affineTransform(img):
    img = np.frombuffer(img, dtype = np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    height, width, _ = img.shape
    detector = cv2.QRCodeDetector()
    (rv, points) = detector.detect(img)
    if rv:
        points = np.float32(points[0])

        trans_points = cv2.minAreaRect(points)
        trans_points = cv2.boxPoints(trans_points)

        trans_points = np.array([trans_points[1], trans_points[2], trans_points[3], trans_points[0]])

        trans_points = np.float32(trans_points)

        matrix = cv2.getPerspectiveTransform(points, trans_points)
        dst = cv2.warpPerspective(img, matrix, (width, height))

        _, enc_image = cv2.imencode('.jpg', dst)
        image_bytes = enc_image.tobytes()

        print(type(image_bytes))
        return image_bytes
    
    else:
        print('exception!')
        raise QRCodeDetection()