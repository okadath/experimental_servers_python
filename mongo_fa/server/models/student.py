from typing import Optional
from pydantic import BaseModel,EmailStr,Field
from bson import ObjectId

class StudentSchema(BaseModel):
    """
    docstring
    """
    fullname:str=Field(...)
    email:EmailStr=Field(...)
    course_of_study:str=Field(...)
    year:int=Field(...,gt=0,lt=9)
    gpa:float=Field(...,le=4.0)

    class Config:
        schema_extra={
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "course_of_study": "Water resources engineering",
                "year": 2,
                "gpa": "3.0",
            }

        } 


class UpdateStudentModel(BaseModel):
    fullname:Optional[str]
    email:Optional[EmailStr]
    course_of_study:Optional[str]
    year:Optional[int]
    gpa:Optional[float]

    class Config:
        schema_extra={
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "course_of_study": "Water resources and environmental engineering",
                "year": 4,
                "gpa": "4.0",
            }
        }

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