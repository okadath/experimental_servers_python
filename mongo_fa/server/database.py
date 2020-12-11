import motor.motor_asyncio


# las definiciones no requieren ningun await

MONGO_DETAILS="mongodb://localhost:27017"

client=motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.studens

student_collection = database.get_collection("students_collection")


def student_helper(student) -> dict:
    return {
        "id":str(student["_id"]),
        "fullname":student["fullname"],
        "email":student["email"],
        "course_of_study":student["course_of_study"],
        "year":student["year"],
        "GPA":student["gpa"],
    }

from bson.objectid import ObjectId

async def retrieve_students():
    students=[]
    async for student in student_collection.find():
        students.append(student_helper(student))
    return students

async def add_student(student_data:dict)->dict:
    student=await student_collection.insert_one(student_data)#ya trae inserted_id?
    new_student= await student_collection.find_one( {"_id":student.inserted_id})
    return student_helper(new_student)


async def retrieve_student(id:str)->dict:
    student= await  student_collection.find_one({"_id":ObjectId(id)})
    if student:
        return student_helper(student)
    return {"error":"no existe"}

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