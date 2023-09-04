# import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import time

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://infusor.store",
    "http://infusor.store:3000",
    "http://infusor.store:8000",
    "http://www.infusor.store",
    "http://www.infusor.store:3000",
    "http://www.infusor.store:8000"
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
    
    return "hello world!"

class ImageStr(BaseModel):
    file: str

@app.post("/api/upload")
async def upload_image(file: ImageStr):
    try:
        image = file.file[file.file.find(",")+1:]
        image = base64.b64decode(image)
        now = time.strftime('%Y%m%d%H%M%S')
        with open(f"images/{now}.jpeg", "wb") as f:
            f.write(image)
        return JSONResponse(content={"message": "Image %s uploaded successfully" % (now + '.jpeg')})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)