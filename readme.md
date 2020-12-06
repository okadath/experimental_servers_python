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

https://www.benjaminpack.com/blog/vs-code-python-pipenv/

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

https://levelup.gitconnected.com/how-to-save-uploaded-files-in-fastapi-90786851f1d3

ya podemos subir imagenes al server y servirlas estaticamente

aun me falta saber como subir las imagenes al statics por medio de la ruta del folder

al aprecer se puede configurar directamente cn nginx y este servira los archivos y demas como cn los deploys de django

para servir staticfiles hay que instalar
install aiofiles

ToDo:

+ guardar a mano(ORM) los mensajes del websocket
+ hacer el server de notificaciones
+ integrar el modelo de usuarios
+ limitar un chat a solo los contactos del usuario
https://blog.nawaz.info/deploy-fastapi-application-on-ubuntu-with-nginx-gunicorn-and-uvicorn
+ admin de fastapi?
+ ORM?
+ integrar los websockets cn vue

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
pytest --cov-report term --cov=main
py.test --cov-report term --cov=. test.py

crear un archivo pytest.ini para configuraciones de los tests y agregar:

```yml
[pytest]
addopts = -p no:warnings
```
