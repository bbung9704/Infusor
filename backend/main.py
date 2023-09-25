import uuid, base64
from affine import Transformer, ImageProcessor, processor
from ml import Unet
import time, cv2

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

@app.get("/api")
async def root():
    try:
        return "connected"

    except Exception as e:
        return e


@app.post("/api/upload")
async def uploadimage(file: UploadFile):
    try:
        image = await file.read()
        file_name = str(uuid.uuid1())
        
        #### 이미지 전처리
        processor = ImageProcessor()
        image = processor.clientToServer(image)
        origin = processor.serverToClient(image)
        ####

        #### Affine transform
        transformer = Transformer(image)
        aff = transformer.Affine(transformer._image)
        affrot = transformer.Rotate(aff)
        ####

        #### 이미지 후처리
        image = processor.serverToClient(affrot)
        ####

        ### 서버 직접 저장
        # with open(f"images/{file_name}.jpeg", "wb") as f:
        #     f.write(image)
        ###

        #### Firebase Storage 저장
        # 원본
        blob = bucket.blob('origins/'+ file_name + '.jpeg')
        blob.upload_from_string(origin, content_type='image/jpeg')

        # 처리
        blob = bucket.blob('images/'+ file_name + '.jpeg')
        blob.upload_from_string(image, content_type='image/jpeg')
        ####

        #### base64 인코딩
        image = base64.b64encode(image)
        ####

        return Response(image)

    except HTTPException as e:
        return JSONResponse( status_code=404, content={ 'message': e.detail } )

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)

class ImageFromFront(BaseModel):
    data: str

@app.post("/api/uploadtest")
async def uploadimagetest(image: ImageFromFront):
    try:
        #### 이미지 전처리
        # processor = ImageProcessor(ratio=0.7)
        image = processor.clientToServerBase64(image.data)
        origin = processor.serverToClient(image)
        ####

        #### Affine transform
        t = Transformer(image)
        centered = t.MoveQrToCenter(t._image)
        aff = t.Perspective(centered)
        affrot = t.Rotate(aff)
        t.reset(affrot)
        constant = t.MakeConstantQr(t._image)
        crop = t.CropInfusor(constant)
        ####
        
        
        #### 이미지 후처리
        image = processor.serverToClient(crop)
        ####

        #### 서버 직접 저장
        with open(f"images/{t.file_name}.jpeg", "wb") as f:
            f.write(image)
        ####

        #### Firebase Storage 저장
        # 원본
        blob = bucket.blob('origins/'+ t.file_name + '.jpeg')
        blob.upload_from_string(origin, content_type='image/jpeg')

        # 처리
        blob = bucket.blob('images/'+ t.file_name + '.jpeg')
        blob.upload_from_string(image, content_type='image/jpeg')
        blob.make_public()
        ####

        #### 23/09/25/18:46 타입 확인
        start = time.time()
        unet = Unet()
        pred = unet.getPrediction(f"images/{t.file_name}.jpeg")
        pred = cv2.resize(pred, dsize=(360,720))
        end = time.time()
        print(f"delta time: {end-start}")
        pred = processor.serverToClient(pred)
        ####

        #### base64 인코딩
        # image = base64.b64encode(image)
        image = base64.b64encode(pred)
        ####

        return Response(image)

    except HTTPException as e:
        return JSONResponse( status_code=404, content={ 'message': e.detail } )

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)