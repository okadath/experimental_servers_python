from typing import List
from fastapi.responses import FileResponse
import databases
import sqlalchemy
from fastapi import FastAPI,File, UploadFile
from pydantic import BaseModel
import shutil
from fastapi.staticfiles import StaticFiles
import os 
parent_dir_path = os.path.dirname(os.path.realpath(__file__))
import uvicorn
from pathlib import Path


current_file = Path(__file__)
current_file_dir = current_file.parent
project_root = current_file_dir.parent
project_root_absolute = project_root.resolve()
static_root_absolute = project_root_absolute / "static"


# SQLAlchemy specific code, as with any other app
# DATABASE_URL = "sqlite:///./test.db"
DATABASE_URL = "sqlite:///data.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
    
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(BaseModel):
    id: int
    text: str
    completed: bool


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/static/img", StaticFiles(directory="static/img"), name="imgs")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/notes/", response_model=List[Note])
async def read_notes():
    query = notes.select()
    return await database.fetch_all(query)


@app.post("/notes/", response_model=Note)
async def create_note(note: NoteIn):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

@app.post("/uploadfile2/")
async def image_up(image: UploadFile = File(...)):
    with open(str(parent_dir_path)+str(image.filename), "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    return {"filename": image.filename}

@app.get("/img/{img}")
async def read_index(img:str):
    # print(image.filename)
    # print( parent_dir_path)
    # print(static_root_absolute) 
    # print(img)
    return FileResponse(os.path.join("static", img))
 
    # return "Hello, world!"

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)