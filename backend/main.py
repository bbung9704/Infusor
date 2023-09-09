import os, uuid, base64, datetime
import affine

# FastAPI
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

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

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# IMG_DIR = os.path.join(BASE_DIR, 'images/')
# SERVER_IMG_DIR = os.path.join('http://localhost:8000/', 'images/')

@app.get("/api")
async def root():
    try:
        return "connected"

    except Exception as e:
        return e
    
class ImageStr(BaseModel):
    file: str

@app.post("/api/upload")
async def upload_image(file: ImageStr):
    try:
        image = file.file[file.file.find(",")+1:]
        image = base64.b64decode(image)
        file_name = str(uuid.uuid1())

        ### 서버 직접 저장
        with open(f"images/test.jpeg", "wb") as f:
            f.write(image)
        ###

        #### db 저장        
        # db.img.insert_one({
        #     "date": datetime.datetime.now(),
        #     "file_name": file_name + '.jpeg',
        #     "url": "images/" + file_name + ".jpeg"
        # })
        ####

        #### Affine transform
        # transformed_img = affine.affineTransform(image)
        ####

        #### Firebase Storage 저장
        blob = bucket.blob('images/'+ file_name + '.jpeg')
        blob.upload_from_string(image, content_type='image/jpeg')
        ####

        return JSONResponse(content={"message": "Image %s uploaded successfully" % (file_name + '.jpeg')})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    

