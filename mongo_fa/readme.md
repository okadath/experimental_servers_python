#manual test cruds fastapi+users+mongo

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




