"""
Extra Models
UNWrapping info here !!!!
Continuing with the previous example, it will be common to have more than one related model.

This is especially the case for user models, because:

The input model needs to be able to have a password.
The output model should not have a password.
The database model would probably need to have a hashed password.

Recap:
Use multiple Pydantic models and inherit freely for each case.

You don't need to have a single data model per entity if that entity must be able to have different "states".
As the case with the user "entity" with a state including password, password_hash and no password.
"""

from typing import Optional, Union, Dict

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


# class UserIn(BaseModel):
#     username: str
#     password: str
#     email: EmailStr
#     full_name: Optional[str] = None
#
#
# class UserOut(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: Optional[str] = None
#
#
# class UserInDB(BaseModel):
#     username: str
#     hashed_password: str
#     email: EmailStr
#     full_name: Optional[str] = None

# Reduce duplication
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):  # user_in is a Pydantic model of class UserIn
    # so user_in.dict() will return dictionary representation of the model
    # and then we passing it into UserInDB (using unwrapping)
    hashed_password = fake_password_hasher(user_in.password)
    # About **user_in.dict()
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


"""
About **user_in.dict() 

UserInDB(**user_dict) it's called unwrapping
where user_dict looks like:
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
means: 
UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)

or more exactly:
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)

SO  Unwrapping a dict And then adding the extra keyword argument
UserInDB(**user_in.dict(), hashed_password=hashed_password)
...ends up being like:

UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    hashed_password = hashed_password,
)

############################################################


Union or anyOf
You can declare a response to be the Union of two types, that means, that the response would be any of the two.
When defining a Union, include the most specific type first, followed by the less specific type. In the example below,
the more specific PlaneItem comes before CarItem in Union[PlaneItem, CarItem].
"""


class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int


items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


# response_model=List[Item]) The same way, you can declare responses of lists of objects
# the more specific PlaneItem comes before CarItem
@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]


# Response with arbitrary dict
# You can also declare a response using a plain arbitrary dict, declaring just the type of the keys and values,
# without using a Pydantic model.
@app.get("/keyword-weights/", response_model=Dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}
