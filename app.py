
import email
from fastapi import FastAPI, Response, status, HTTPException, Header, Query, Path
from starlette.datastructures import MutableHeaders
from pydantic import BaseModel
from typing import Optional, List
from models import Fitness
from database import SessionLocal
import models, json

app = FastAPI()


class Item(BaseModel):
    id: int
    name: str
    description: str
    price: int
    on_offer: bool

    class Config:
        orm_mode = True


class Person(BaseModel):
    id: Optional[int] = None
    email: str
    passwordFB: str
    name: str
    age: int
    gender: str

with open("people.json", "r") as f:
    people = json.load(f)#["people"]


@app.post("/fit", response_model=Fitness, status_code=status.HTTP_201_CREATED)
async def create_an_item(item: Fitness):
    print(type(item))
    print(item.avocado)


app.get("/people/{p_id}", status_code=200)
def get_person(p_id: int):
    person = [p for p in people if p["id"]==p_id]
    return person[0] if len(person) > 0 else {}

@app.get("/search", status_code=200)
def search_person(age: Optional[int] = Query(None, title="Age", description="The age to filter for"),
                    name: Optional[str] = Query(None, title="Name", description="The name for filter")):
    people1= [p for p in people if p["age"] == age]
    if name is None:
        if age is None:
            return people
        else:
            return people
    else:
        people2 = [p for p in people if name.lower() in p["name"].lower()]
        if age is None:
            return people2
        else:
            combined = [p for p in people1 if p in people2]
            return combined

@app.post("/addPerson", status_code=201)
def add_peron(person: Person):
    p_id = max([p["id"] for p in people] + 1)
    new_person = {
        "id": p_id,
        "email": person.email,
        "passwordFB": person.passwordFB,
        "name": person.name,
        "age": person.age,
        "gender": person.gender
    }
    people.append(new_person)
    with open("people.json", "w") as f:
        json.dump("people", f)
    
@app.put("/changePerson", status_code=204)
def change_person(person: Person):
    new_person = {
        "id": person.id,
        "email": person.email,
        "passwordFB": person.passwordFB,
        "name": person.name,
        "age": person.age,
        "gender": person.gender
    }
    person_list = [p for p in people if p["id"] == person.id]
    if len(person_list) > 0:
        people.remonve(person_list[0])
        people.append(new_person)
        with open("people.json", "w") as f:
            json.dump(people, f)
        return new_person
    else:
        return HTTPException(status_code=404, detail=f"Person with id {person.id} does not exist!")

app.delete("/deletePerson/{p_id}", status_code=204)
def delete_person(p_id: int):
    person = [p for p in people if p["id"] == p_id]
    if len(person) > 0:
        people.remove(person[0])
        with open("people.json", "w") as f:
            json.dump(people, f)
    else:
        raise HTTPException(status_code=404, detail=f"There is no person with id {p_id}")


#print(people)

db = SessionLocal()


@app.post("/retrofit", response_model=Item, status_code=status.HTTP_200_OK)
async def update_an_item(item: Item):
    print(item)
    return item


@app.get("/items", response_model=List[Item], status_code=200)
async def get_all_items():
    items = db.query(models.Item).all()
    return items


@app.get("/item/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
async def get_an_item(item_id: int, Authorization: str = Header(None)):
    # kk  = MutableHeaders(x_token.headers)
    print({"User-Agent": Authorization})
    print(type(Header))
    print("--------------")
    item = db.query(models.Item).filter(models.Item.id == item_id).first()

    return item


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_an_item(item: Item):
    print(type(item))
    db_item = db.query(models.Item).filter(
        models.Item.name == item.name).first()
    if db_item is not None:
        raise HTTPException(status_code=400, detail="Item already exist")

    new_item = models.Item(

        id=int(item.name),
        name=item.name,
        price=item.price,
        description=item.description,
        on_offer=item.on_offer,
    )

    db.add(new_item)
    db.commit()
    return new_item


@app.put("/item/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
async def update_an_item(item_id: int, item: Item):
    print(item)
    item_to_update = db.query(models.Item).filter(
        models.Item.id == item_id).first()
    item_to_update.name = item.name
    item_to_update.price = item.price
    item_to_update.description = item.description
    item_to_update.on_offer = item.on_offer

    db.commit()
    return item_to_update


@app.delete("/item/{item_id}")
async def delete_item(item_id: int):
    item_to_delete = db.query(models.Item).filter(
        models.Item.id == item_id).first()

    if item_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resourse not Found")

    db.delete(item_to_delete)
    db.commit()

    return item_to_delete


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# @app.get("/greet/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": f"Hello {item_id}"}


# @app.get("/greet")
# async def greet_optional_name(name:Optional[str]="user"):
#     return {"greeting": f"Hello {name}"}


# @app.put("/item/{item_id}")
# async def update_item(item_id:int, item:Item):
#     print(f"Item {item}")
#     return {"name":item.name,
#             "description":item.description,
#             "price":item.price,
#             "on_offer":item.on_offer,
#             }
