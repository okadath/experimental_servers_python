# fastAPI

instalar:

```sh
pipenv install fastapi[all]
```

correr con:

```sh
uvicorn nombrearchivo:nombre_server(x default app) --reload
```

para correr pipenv en vscode

<https://www.benjaminpack.com/blog/vs-code-python-pipenv/>

en el ambiente corres

```sh
pipenv --py
```

te devolvera un path cn la ruta del ambiente

creas un folder:

```sh
mkdir .vscode && touch .vscode/settings.json
```

y agregas lo siguinete al archivo de configuracion, poniendo el path:

```js
{
    "files.exclude": {
        "**/.git": true,
        "**/.svn": true,
        "**/.hg": true,
        "**/CVS": true,
        "**/.DS_Store": true,
        "**/*.pyc": true,
        "**/__pycache__": true
    },
    "python.pythonPath": "<VIRTUALENV_PYTHON_PATH_HERE>"
}
```

lo indicas en la paleta de comandos en select interpreter

e instalas el linter de python

```sh
pipenv install --dev pylint
```

<https://levelup.gitconnected.com/how-to-save-uploaded-files-in-fastapi-90786851f1d3>

ya podemos subir imagenes al server y servirlas estaticamente

aun me falta saber como subir las imagenes al statics por medio de la ruta del folder

al aprecer se puede configurar directamente cn nginx y este servira los archivos y demas como cn los deploys de django

para servir staticfiles hay que instalar
install aiofiles

## Django+Mongo DB = Djongo

hay que instalar mongo en ubuntu, y mongo compass para importar la info:

mongo guarda sus archivos en la siguiente direccion:

cat /var/lib/mongodb/
como archivos collection-7-6296793190435309642.wt

```py
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'admin',
    }
}
```

la db debe de llmarse admin o si no habra errores con el sistema de usuarios(x lo mismo necesita una instalacion local de mongo, por que mongo solo tiene una db con ese nombre por default, o se ensimara con la de multiples proyectos)

hay que migrar la primera vez para que genere la info del modelo de usuarios
python manage.py migrate

### instalando mongo y mongo compass

mongo se instala directamente del apt, mongo compass debe obtenerse el instalador descargandolo, las versiones superiores al 1.15 presentan problemas de dependencia, resolver con sudo apt --fix-broken install

```sh
wget https://downloads.mongodb.com/compass/mongodb-compass_1.23.0_amd64.deb
sudo dpkg -i mongodb-compass_1.23.0_amd64.deb
mongodb-compass;
```

desde ahi se pueden hacer importaciones/exportaciones como con el modulo import export con django a partir de un csv

uvicorn users_fast:app --reload --host 0.0.0.0 --port 5000

## Testing

instalar

```shell
pipenv install pytest coverage  pytest-cov  
```

y ejecutar para ver los errores

```sh
pytest --cov-report term --cov=main
py.test --cov-report term --cov=. test.py
```

crear un archivo pytest.ini para configuraciones de los tests y agregar:

```yml
[pytest]
addopts = -p no:warnings
```

creo que usaremos mongo x su facilidad de escalado, pero tendre que resolver a mano el problema de delete on cascade, para escalar estos servers al parecer mongo internamente usa algo llamado Sharded Cluster que distribuye la informacion entre varias instancias horizontalmente(el escalado vertical es darle mas recursos a una maquina)
aun necesito investigar el ORM Motor que es mongo asincrono para python, aunque quiza y asi lo dejo
por que no hay gran diferencia en fast api, pero no se si en el modelo de usuarios

necesito analizar las operiaciones de FK criticas apra diseñar correctamente esta o futuras coleciones en mongo  

al parecer se puede usar correctamente con Motor usandolo segun la documentacion de fastapi users, solo hay que usar las collections correctas

funciones en motor(casi iguales a als de cualquier ORM)
<https://motor.readthedocs.io/en/stable/tutorial-asyncio.html>

se me ocurre hacer una lista de ids por cada elemento dependiente y en el en cascada borrarlo pero me parecce que no es una operacion critica, se dejarian vivas las cosas commo  comentarios, chats, tags, quiza hasta las fotos , pero quiza si habria de hacerlo con los posts y con fotos, quiza hasta videos, es mejor usar almacenamiento local para fotos y videso y en la db solo almacenar rutas, asi me parece que no seria necesario hacer algun join o algo asi
supongo que tendre que indicar que el usuario elimino su perfil

creo que hacer un admin desde cierto punto es impractico, pero por si acaso hay que tratar de hacerlo con vue, necesitaria algun tipo de scaffolding

ejemplos fastapi mongo
<https://github.com/Youngestdev/async-fastapi-mongo>
<https://github.com/rbcabreraUPM/fastapi-basic-mongodb-example>

ejemplo proyecto
<https://testdriven.io/blog/fastapi-mongo/#mongodb>

creo que si hay pks voy a tener que insertar los ids, pero si se borra el elemento de la pk tendre que hacer alguna validacion a mano indicando que no existe por la falta de cascada
<https://docs.mongodb.com/manual/core/data-model-design/#data-modeling-referencing>

eventbrite usa mongo
<https://es.slideshare.net/interviewcoach/building-a-social-network-with-mongodb-74467821>

correr si esta en carpetas como si estuviera en paquete, como gunicorn, con . :

```sh
uvicorn example_db.main:app --reload --host 0.0.0.0 --port 8000
```

## manual test cruds fastapi+users+mongo

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

si se necesita authorization se usa el paquete de fast api users
y a partir de el en las funciones del router
se agregan las dependencias:

<https://frankie567.github.io/fastapi-users/usage/dependency-callables/>

```py
from fastapi import FastAPI

app = FastAPI()
fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

router = APIRouter()
from fastapi import   HTTPException
from fastapi import Depends

@router.get("/{id}", response_description="Profile data retrieved")
async def get_profile_data(id:str,user: User = Depends(fastapi_users.get_current_user)):
    ...

app.include_router(router, tags=["Profile"], prefix="/profile")

```

agregar files:

install python-multipart

para evaluar si la funcion es una imagen:

```py
from fastapi import FastAPI, File, UploadFile
import shutil
import imghdr

@app.post("/savefile/")
async def image(image: UploadFile = File(...)):
    print(imghdr.what(image.file))
```

para pagos usaremos stripe como en flask

se ve como paypal pero mas facil

<https://testdriven.io/blog/flask-stripe-tutorial/>

### sockets

var ws = new WebSocket("ws://67.205.154.215/ws");

## ToDo

+ guardar a mano(ORM) los mensajes del websocket
+ hacer el server de notificaciones  
+ integrar los websockets cn vue
+ probar sockets con el deploy y un dominio

## por completar(no es de muerte)

+ hay pequeñas funcionalidades de video que arreglar
+ integrar la validacion y miniaturizacion de imagenes
+ uuid
+ deploy <https://blog.nawaz.info/deploy-fastapi-application-on-ubuntu-with-nginx-gunicorn-and-uvicorn>

ejecutandolo con  gunicorn hay mayor performance
hay que usar artillery instalandolo en yarn

hay que crear un yaml con la configuracion del test

```yaml
config:
    target: "ws://localhost:8000/ws"
    ensure:
      maxErrorRate: 3
    phases:
      - duration: 200
        arrivalRate: 220
        name: "Max load"
scenarios:
  - engine: "ws"
    flow:
      - loop:
          - send: "hello"
          - think: 5
        count: 40
```

```yml
config:
    target: "ws://localhost:8000/ws"
    ensure:
      maxErrorRate: 3
    phases:
      - duration: 240
        arrivalRate: 200
        name: "Max load"
scenarios:
  - engine: "ws"
    flow:
      - send: "hello"
      - think: 80
      - send: "how are you?"
      - think: 80
      - send: "how are you?"
      - think: 80
      - send: "how are you?"
```   

para ejecutar el test:

```sh
yarn artillery run loadtest.yml --output result_13.json
```

para visualizarlo en grafixos

```bash
yarn artillery report result_12.json 
```

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker ws_docs:app
```

IG inicio sin chat, no hasta marzo del 2013, salio en septiembre 2012, alcanzo 1 millon en 2 meses, alcanzo 20 millones en un año

importa mas el server de notificaciones creo

alcanza aproximadamente 25-28k de usuarios(x2, no se por que los duplica el test) antes de caerse, sin gunicorn solo aguanta 7(x2) concurrentes, y las peticiones las sigue manejando bien

quiza haya que hacer un socket activable al abrirla pero aun asi no se que ocurra con todas las notificaciones

checar si vue jala bien con ionic, tambien si lo compila, y si es asi las webnotifications