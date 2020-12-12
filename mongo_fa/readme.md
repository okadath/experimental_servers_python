# manual test cruds fastapi+users+mongo

instalar

```sh
pipenv install pydantic[email] motor
```

para saber el puerto de mongo

```sh
mongo
db.serverCmdLineOpts()

#o

sudo lsof -iTCP -sTCP:LISTEN | grep mongo
```

ejecutar con

```sh
uvicorn mongo_fa.main:app --reload --host 0.0.0.0 --port 8000
```

pyndatic no tiene por que validar otros tipos de datos
asi que cosas como el ObjectId lo tengo que hacer yo

si el id no es del tipo, truena el server, hay que hacer la siguiente validacion en database.py:

```py
from bson.objectid import ObjectId

async def retrieve_student(id:str)->dict:
    if ObjectId.is_valid(id):
        student= await  student_collection.find_one({"_id":ObjectId(id)})
        if student:
            return student_helper(student)
    return {"error":"error"}
```

y esta debe ser validada en la ruta a evaluar, lanzando una excepcion en caso de error:

```py
from fastapi import   HTTPException

@router.get("/{id}", response_description="Student data retrieved")
async def get_student_data(id:str):
    student = await retrieve_student(id)
    if student=={"error":"error"}:
        raise HTTPException(status_code=404, detail="Student doesn't exist.")
    if student:
        return ResponseModel(student, "Student data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")
```
