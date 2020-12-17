
from fastapi import FastAPI

from .routes.student import router as StudentRouter
from .routes.profile import router as ProfileRouter

app = FastAPI()

app.include_router(StudentRouter, tags=["Student"], prefix="/student")

app.include_router(ProfileRouter, tags=["Profile"], prefix="/profile")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}


from fastapi import FastAPI, File, UploadFile
import shutil
import imghdr

@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}


@app.post("/savefile/")
async def image(image: UploadFile = File(...)):
    print(imghdr.what(image.file))
    with open(str(image.filename), "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)        
    
    return {"filename": image.filename}