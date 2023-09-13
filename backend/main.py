import uuid, base64
import numpy as np
from affine import Transformer, ImageProcessor

# FastAPI
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse, Response
from starlette.middleware.cors import CORSMiddleware

# # DB
# from pymongo import MongoClient

# Firebase Storage
import firebase_admin
from firebase_admin import credentials, storage

# Firebase Storage
cred = credentials.Certificate('key/serviceKey.json')
firebase_admin.initialize_app(cred)
bucket = storage.bucket('infuser-7a7c8.appspot.com')


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

        # 변형
        blob = bucket.blob('images/'+ file_name + '.jpeg')
        blob.upload_from_string(image, content_type='image/jpeg')
        ####

        image = base64.b64encode(image)
        
        return Response(image)

    except HTTPException as e:
        return JSONResponse( status_code=404, content={ 'message': e.detail } )

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=404)
    

