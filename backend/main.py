import uuid, base64
from affine import Transformer, ImageProcessor, processor
from ml import Unet
import cv2
import numpy as np

# FastAPI
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse, Response
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# # DB
# from pymongo import MongoClient

# Firebase Storage
from firebase import fireBaseStorage

# Firebase Storage
bucket = fireBaseStorage.bucket

# # DB
# client = MongoClient(os.environ.get("MONGO_DB_PATH"))
# db = client.imageSet

# APP
app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://infusor.store",
    "http://infusor.store:3000",
    "http://infusor.store:8000",
    "http://www.infusor.store",
    "http://www.infusor.store:3000",
    "http://www.infusor.store:8000",
    "https://infusor.store",
    "https://infusor.store:3000",
    "https://infusor.store:8000",
    "https://www.infusor.store",
    "https://www.infusor.store:3000",
    "https://www.infusor.store:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#### Model
class ImageFromFront(BaseModel):
    data: str
####

@app.get("/api")
async def root():
    try:
        return "connected"

    except Exception as e:
        return e


@app.post("/api/upload")
async def uploadimage(image: ImageFromFront):
    try:
        #### 이미지 전처리
        # processor = ImageProcessor(ratio=1)
        image = processor.clientToServerBase64(image.data)
        origin = processor.serverToClient(image)
        ####

        #### Transform
        t = Transformer(image)
        centered = t.MoveQrToCenter(t._image)
        aff = t.Perspective(centered) # or t.Affine(centered)
        affrot = t.Rotate(aff)
        t.reDetectQrCoordinate(affrot)
        constant = t.MakeConstantQr(t._image)
        crop = t.CropInfusor(constant)
        ####
        
        
        #### 이미지 후처리
        image = processor.serverToClient(crop)
        ####

        # #### 23/09/25/18:46 ML 모델 사용
        # unet = Unet()
        # pred = unet.getPrediction(crop)
        # pred = cv2.resize(pred, dsize=(360,720))
        # pred[np.where((pred==[255, 255, 255]).all(axis=2))] = [0, 0, 255]
        # pred = cv2.addWeighted(crop, 0.7, pred, 0.3, 0)
        # pred = processor.serverToClient(pred)
        # ####

        #### Firebase Storage 저장
        # Origin
        blob = bucket.blob('origin/'+ t.file_name + '.jpeg')
        blob.upload_from_string(origin, content_type='image/jpeg')

        # Transformed
        blob = bucket.blob('images/'+ t.file_name + '.jpeg')
        blob.upload_from_string(image, content_type='image/jpeg')
        blob.make_public()
        
        # # ML Pred with mask
        # blob = bucket.blob('predict/'+ t.file_name + '.jpeg')
        # blob.upload_from_string(pred, content_type='image/jpeg')
        # blob.make_public()
        # ####

        return Response(blob.public_url)

    except HTTPException as e:
        return JSONResponse( status_code=404, content={ 'message': e.detail } )

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)


@app.post("/api/uploadtest")
async def uploadimagetest(image: ImageFromFront):
    try:
        #### 이미지 전처리
        # processor = ImageProcessor(ratio=1)
        image = processor.clientToServerBase64(image.data)
        origin = processor.serverToClient(image)
        ####

        #### Transform
        t = Transformer(image)
        centered = t.MoveQrToCenter(t._image)
        aff = t.Perspective(centered) # or t.Affine(centered)
        affrot = t.Rotate(aff)
        t.reDetectQrCoordinate(affrot)
        constant = t.MakeConstantQr(t._image)
        crop = t.CropInfusor(constant)
        ####
        
        
        #### 이미지 후처리
        image = processor.serverToClient(crop)
        ####

        #### 23/09/25/18:46 ML 모델 사용
        unet = Unet()
        pred = unet.getPrediction(crop)
        pred = cv2.resize(pred, dsize=(360,720))
        pred[np.where((pred==[255, 255, 255]).all(axis=2))] = [0, 0, 255]
        pred = cv2.addWeighted(crop, 0.7, pred, 0.3, 0)
        pred = processor.serverToClient(pred)
        ####

        #### Firebase Storage 저장
        # Origin
        blob = bucket.blob('origin/'+ t.file_name + '.jpeg')
        blob.upload_from_string(origin, content_type='image/jpeg')

        # Transformed
        blob = bucket.blob('images/'+ t.file_name + '.jpeg')
        blob.upload_from_string(image, content_type='image/jpeg')
        blob.make_public()
        
        # ML Pred with mask
        blob = bucket.blob('predict/'+ t.file_name + '.jpeg')
        blob.upload_from_string(pred, content_type='image/jpeg')
        blob.make_public()
        ####

        return Response(blob.public_url)

    except HTTPException as e:
        return JSONResponse( status_code=404, content={ 'message': e.detail } )

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)