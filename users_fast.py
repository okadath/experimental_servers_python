# import databases
# import sqlalchemy
# from fastapi import FastAPI, Request
# from fastapi_users import FastAPIUsers, models
# from fastapi_users.authentication import JWTAuthentication
# from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
# from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base


# from fastapi import Depends, Response

# DATABASE_URL = "sqlite:///data.db"
# SECRET = "SECRET"


# class User(models.BaseUser):
#     pass


# class UserCreate(models.BaseUserCreate):
#     pass


# class UserUpdate(User, models.BaseUserUpdate):
#     pass


# class UserDB(User, models.BaseUserDB):
#     pass


# database = databases.Database(DATABASE_URL)
# Base: DeclarativeMeta = declarative_base()


# class UserTable(Base, SQLAlchemyBaseUserTable):
#     pass


# engine = sqlalchemy.create_engine(
#     DATABASE_URL, connect_args={"check_same_thread": False}
# )
# Base.metadata.create_all(engine)

# users = UserTable.__table__
# user_db = SQLAlchemyUserDatabase(UserDB, database, users)


# def on_after_register(user: UserDB, request: Request):
#     print(f"User {user.id} has registered.")


# def on_after_forgot_password(user: UserDB, token: str, request: Request):
#     print(f"User {user.id} has forgot their password. Reset token: {token}")


# jwt_authentication = JWTAuthentication(
#     secret=SECRET, lifetime_seconds=3600, tokenUrl="/auth/jwt/login"
# )

# app = FastAPI()
# fastapi_users = FastAPIUsers(
#     user_db,
#     [jwt_authentication],
#     User,
#     UserCreate,
#     UserUpdate,
#     UserDB,
# )


# # app.include_router(
# #     fastapi_users.get_register_router(refresh_jwt), prefix="/auth/jwt/refresh", tags=["auth"]
# # )

# app.include_router(
#     fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
# )
# app.include_router(
#     fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
# )
# app.include_router(
#     fastapi_users.get_reset_password_router(
#         SECRET, after_forgot_password=on_after_forgot_password
#     ),
#     prefix="/auth",
#     tags=["auth"],
# )
# app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])


# @app.on_event("startup")
# async def startup():
#     await database.connect()


# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()






# @app.post("/auth/jwt/refresh")
# async def refresh_jwt(response: Response, user=Depends(fastapi_users.get_current_active_user)):
#     print(user)
#     print(response)
#     return await jwt_authentication.get_login_response(user, response)



from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")