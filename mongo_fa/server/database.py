import motor.motor_asyncio


# las definiciones no requieren ningun await

MONGO_DETAILS="mongodb://localhost:27017"

client=motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.studens

student_collection = database.get_collection("students_collection")
profile_collection = database.get_collection("profiles_collection")

student_collection.create_index("fullname", unique=True)
# database.command(db.collection_name.createIndex( {field_name : 1} , {unqiue : true} ))

def student_helper(student) -> dict:
    return {
        "id":str(student["_id"]),
        "fullname":student["fullname"],
        "email":student["email"],
        "course_of_study":student["course_of_study"],
        "year":student["year"],
        "GPA":student["gpa"],
    }

def profile_helper(profile) -> dict:
    return {
        "id":str(profile["_id"]),
        "pic":profile["pic"],
        "user":str(profile["user"]),
    }

from bson.objectid import ObjectId

async def retrieve_students():
    students=[]
    async for student in student_collection.find():
        students.append(student_helper(student))
    return students

async def add_student(student_data:dict)->dict:
    try:
        student=await student_collection.insert_one(student_data)#ya trae inserted_id?
        profile=await profile_collection.insert_one({
            "user":student.inserted_id,
            "pic":"",
            })
    except  Exception as e:
        print(e)
        # raise e
        return []
    new_student= await student_collection.find_one( {"_id":student.inserted_id})
    # profile=await profile_collection.insert_one(profile_data)
    return student_helper(new_student)

# async def add_profile(profile_data:dict)->dict:
#     try:
#         profile=await profile_collection.insert_one(profile_data)#ya trae inserted_id?
#     except  Exception as e:
#         print(e)
#         # raise e
#         return []
#     new_profile= await profile_collection.find_one( {"_id":profile.inserted_id})
#     return profile_helper(new_profile)


async def retrieve_student(id:str)->dict:
    if ObjectId.is_valid(id):
        student= await  student_collection.find_one({"_id":ObjectId(id)})
        if student:
            return student_helper(student)
    return {"error":"error"}

async def update_student(id:str,data:dict):
    if len(data)<1:
        return False
    student=await student_collection.find_one({"_id":ObjectId(id)})
    if student:
        update_student=await student_collection.update_one(
            {"_id":ObjectId(id)},{"$set":data}
        )
    if update_student:
        return True
    return False

async def delete_student(id:str):
    student=await student_collection.find_one({"_id":ObjectId(id)})
    if student:
        await student_collection.delete_one({"_id":ObjectId(id)})
        return True
    return False



async def retrieve_profiles():
    profiles=[]
    async for profile in profile_collection.find():
        profiles.append(profile_helper(profile))
    return profiles


async def retrieve_profile(id:str)->dict:
    if ObjectId.is_valid(id):
        profile= await  profile_collection.find_one({"_id":ObjectId(id)})
        if profile:
            return profile_helper(profile)
    return {"error":"error"}

async def update_profile(id:str,data:dict):
    if len(data)<1:
        return False
    profile=await profile_collection.find_one({"_id":ObjectId(id)})
    if profile:
        update_profile=await profile_collection.update_one(
            {"_id":ObjectId(id)},{"$set":data}
        )
    if update_profile:
        return True
    return False

async def delete_profile(id:str):
    profile=await profile_collection.find_one({"_id":ObjectId(id)})
    if profile:
        await profile_collection.delete_one({"_id":ObjectId(id)})
        return True
    return False