# def get_full_name(first_name: str, last_name: str):
#     full_name = first_name.title() + " " + last_name.title() 
#     return full_name


# print(get_full_name("john", "doe"))

# def get_name_with_age(name: str, age: int):
#     name_with_age = name + " is this old: " + str(age)
#     return name_with_age

# def get_items(item_a: str, item_b: int, item_c: float, item_d: bool, item_e: bytes):
#     return item_a, item_b, item_c, item_d, item_d, item_e

# from typing import List


# def process_items(items: List[str]):
#     for item in items:
        
#         print(item)


# from typing import Set, Tuple


# def process_items(items_t: Tuple[int, int, str], items_s: Set[bytes]):
#     return items_t, items_s

# from typing import Dict


# def process_items(prices: Dict[str, float]):
#     for item_name, item_price in prices.items():
#         print(item_name)
#         print(item_price)


# from typing import Optional


# def say_hi(name: Optional[str] = None):
#     if name is not None:
#         print(f"Hey {name}!")
#     else:
#         print("Hello World")

# class Person:
#     def __init__(self, name: str):
#         self.name = name


# def get_person_name(one_person: Person):
#     return one_person


# from datetime import datetime
# from typing import List, Optional

# from pydantic import BaseModel


# class User(BaseModel):
#     id: int
#     name = "John Doe"
#     signup_ts: Optional[datetime] = None
#     friends: List[int] = []


# external_data = {
#     "id": "123",
#     "signup_ts": "2017-06-01 12:22",
#     "friends": [1, "2", b"3"],
# }
# user = User(**external_data)
# print(user)
# # > User id=123 name='John Doe' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3]
# print(user.id)

from enum import Enum

from fastapi import FastAPI, Query,Body,Cookie

from typing import Optional

from typing import List

from pydantic import BaseModel


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}




class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None



@app.post("/itemsss/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.put("/itemss/{item_id}")
async def create_item2(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

@app.get("/items/")
async def read_items(q: str = Query(..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/itemsa/")
async def read_items2(q: Optional[List[str]] = Query(None)):
    query_items = {"q": q}
    return query_items


@app.get("/itemsq/")
async def read_items3(
    q: Optional[str] = Query(
        None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results



class User(BaseModel):
    username: str
    full_name: Optional[str] = None


@app.put("/itemscc/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results

@app.put("/itemsvv/{item_id}")
async def update_item2(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: int = Body(..., gt=0),
    q: Optional[str] = None
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results

@app.get("/itemffs/")
async def read_items4(ads_id: Optional[str] = Cookie(None)):
    return {"ads_id": ads_id}