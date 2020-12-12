from fastapi.testclient import TestClient

from example_test import app

client = TestClient(app)


def test_create_user():
    response = client.post("/auth/register", 
        json=
        {
  "email": "asd@example.com",
  "password": "string",
  #usa True y False aqui en mayusculas pero en la api debemos pasarlo en minusculas
  "is_active": True,
  "is_superuser": False
}
    )
    assert response.status_code == 201#creado
    print(response.json())


    # assert response.json() == {
    #     "id": "foobar",
    #     "title": "Foo Bar",
    #     "description": "The Foo Barters",
    # }
import shutil, os, glob
def test_delete_db():
    files = glob.glob(os.getcwd()) 
    os.remove(os.getcwd()+'/data_test.db')