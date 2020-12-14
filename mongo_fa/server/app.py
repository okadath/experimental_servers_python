
from fastapi import FastAPI

from .routes.student import router as StudentRouter
from .routes.profile import router as ProfileRouter

app = FastAPI()

app.include_router(StudentRouter, tags=["Student"], prefix="/student")

app.include_router(ProfileRouter, tags=["Profile"], prefix="/profile")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}