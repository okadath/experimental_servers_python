import motor.motor_asyncio
from fastapi import FastAPI, Request
from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import MongoDBUserDatabase

DATABASE_URL = "mongodb://localhost:27017"
SECRET = "SECRET"


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client["database_name"]
collection_users = db["users"]
collection_profiles = db["profiles"]
user_db = MongoDBUserDatabase(UserDB, collection_users)

collection_profiles.create_index("user", unique=True)

def profile_helper(profile) -> dict:
    return {
        "id":str(profile["_id"]),
        "pic":profile["pic"],
        "user":str(profile["user"]),
    }

from bson.objectid import ObjectId



async def on_after_register(user: UserDB, request: Request):
    try:
        # uuser=await collection_users.insert_one(user)#ya trae inserted_id?
        profile=await collection_profiles.insert_one({
            "user":user.id,
            "pic":"",
            })
    except  Exception as e:
        # print(e)
        raise e
        return []
    print(f"User {user.id} has registered.")


def on_after_forgot_password(user: UserDB, token: str, request: Request):

    print(f"User {user.id} has forgot their password. Reset token: {token}")


jwt_authentication = JWTAuthentication(
    secret=SECRET, lifetime_seconds=3600, tokenUrl="/auth/jwt/login"
)

app = FastAPI()
fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)
app.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_reset_password_router(
        SECRET, after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])


from typing import Optional
from pydantic import BaseModel,EmailStr,Field
from bson import ObjectId


async def retrieve_profiles():
    profiles=[]
    async for profile in collection_profiles.find():
        profiles.append(profile_helper(profile))
    return profiles


async def retrieve_profile(id:str)->dict:
    if ObjectId.is_valid(id):
        profile= await  collection_profiles.find_one({"_id":ObjectId(id)})
        if profile:
            return profile_helper(profile)
    return {"error":"error"}



#extend profile:
class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

class ProfileSchema(BaseModel):
    pic:str=Field(...) 
    user: Optional[PyObjectId] = Field(alias='user') 

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra={
            "example": {
                "user": "5fd5158379f15ab4c0693f7f",
                "pic": "/asd.jpg", 
            }

        }
 

class UpdateProfileModel(BaseModel):
    pic:str=Field(...) 
    user: Optional[PyObjectId] = Field(alias='user') 

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra={
            "example": {
                "user": "5fd5158379f15ab4c0693f7f",
                "pic": "/asd.jpg", 
            }
        }

def ResponseModel(data,message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}


from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder


router = APIRouter()
from fastapi import   HTTPException
from fastapi import Depends

# @router.post("/", response_description="Profile data added into the database")
# async def add_student_data(profile: ProfileSchema = Body(...)):
#     profile = jsonable_encoder(profile)
#     new_profile = await add_profile(profile)
#     if new_profile==[]:
#         raise HTTPException(status_code=404, detail="Profile name already exists")
#     return ResponseModel(new_profile, "Profile added successfully.")


@router.get("/", response_description="Profiles retrieved")
async def get_profiles():
    profiles = await retrieve_profiles()
    if profiles:
        return ResponseModel(profiles, "Profiles data retrieved successfully")
    return ResponseModel(profiles, "Empty list returned")


@router.get("/{id}", response_description="Profile data retrieved")
async def get_profile_data(id:str,user: User = Depends(fastapi_users.get_current_user)):
    profile = await retrieve_profile(id)
    if profile=={"error":"error"}:
        raise HTTPException(status_code=404, detail="Profile doesn't exist.")
    if profile:
        return ResponseModel(profile, "Profile data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Profile doesn't exist.")

app.include_router(router, tags=["Profile"], prefix="/profile")


# @router.put("/{id}")
# async def update_profile_data(id:str,req:UpdateProfileModel=Body(...)):
#     req={k:v for k,v in req.dict().items() if v is not None}
#     updated_profile=await update_profile(id,req)
#     if updated_profile:
#         return ResponseModel(
#             "Profile with ID: {} name update is successful".format(id),
#             "Profile name updated successfully",
#         )
#     return ErrorResponseModel(
#         "An error occurred",
#         404,
#         "There was an error updating the profile data.",
#     )

# @router.delete("/{id}",response_description="Profile data deleted from the database")
# async def delete_profile_data(id:str):
#     deleted_profile=await delete_profile(id)
#     if deleted_profile:
#         return ResponseModel(
#             "Profile with ID: {} removed".format(id), "Profile deleted successfully"
#         )
#     return ErrorResponseModel(
#         "An error occurred", 404, "Profile with id {0} doesn't exist".format(id)
#     )