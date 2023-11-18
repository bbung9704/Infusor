
from affine import Transformer, processor
from ml_model.ml import ML_Model
from predict_volume import predict_volume
from util import get_time
import cv2
import numpy as np

# FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, Response
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# # DB
# from pymongo import MongoClient

# Firebase Storage
from firebase import fireBase

# Firebase
bucket = fireBase.bucket
db = fireBase.db

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

# ML 모델 예측 포함 출력
@app.post("/api/upload")
async def uploadimage(image: ImageFromFront):
    try:
        #### 이미지 전처리
        image = processor.clientToServerBase64(image.data)
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
        
        #### image segmentation
        model = ML_Model()
        pred_binary = model.getPrediction(crop)
        pred_binary = cv2.resize(pred_binary, dsize=(360,720))
        pred = model.binary2color(pred_binary)
        pred[np.where((pred==[255, 255, 255]).all(axis=2))] = [0, 0, 255]
        pred = cv2.addWeighted(crop, 0.7, pred, 0.3, 0)
        pred = processor.serverToClient(pred)
        ####

        #### volume prediction
        volume = predict_volume(pred_binary)
        ####

        # ML Pred with mask
        blob = bucket.blob('predict/'+ t.file_name + '.jpeg')
        blob.upload_from_string(pred, content_type='image/jpeg')
        blob.make_public()
        ####

        res = {
            "url": blob.public_url,
            "volume": volume,
            "time": fireBase.timestamp(),
        }

        db.collection("predictions").add(res)

        res["time"] = get_time()

        return res

    except HTTPException as e:
        return JSONResponse( status_code=404, content={ 'message': e.detail } )

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)

@app.get("/api/pred")
async def prediction_list():
    try:
        pred_ref = db.collection("predictions")
        query = pred_ref.order_by("time", direction=fireBase.reverse()).limit(10)
        objs = [obj.to_dict() for obj in query.stream()]
        json = {"data": objs}    

        return json
    
    except Exception as e:
        return e