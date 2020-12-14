from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    # add_profile,
    delete_profile,
    retrieve_profile,
    retrieve_profiles,
    update_profile,
)
from server.models.student import (
    ProfileSchema,
    UpdateProfileModel,
     ErrorResponseModel,
     ResponseModel,
)

router = APIRouter()
from fastapi import   HTTPException


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
async def get_profile_data(id:str):
    profile = await retrieve_profile(id)
    if profile=={"error":"error"}:
        raise HTTPException(status_code=404, detail="Profile doesn't exist.")
    if profile:
        return ResponseModel(profile, "Profile data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Profile doesn't exist.")


@router.put("/{id}")
async def update_profile_data(id:str,req:UpdateProfileModel=Body(...)):
    req={k:v for k,v in req.dict().items() if v is not None}
    updated_profile=await update_profile(id,req)
    if updated_profile:
        return ResponseModel(
            "Profile with ID: {} name update is successful".format(id),
            "Profile name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the profile data.",
    )

@router.delete("/{id}",response_description="Profile data deleted from the database")
async def delete_profile_data(id:str):
    deleted_profile=await delete_profile(id)
    if deleted_profile:
        return ResponseModel(
            "Profile with ID: {} removed".format(id), "Profile deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Profile with id {0} doesn't exist".format(id)
    )