"""
Response Model
You can declare the model used for the response with the parameter response_model in any of the path operations

It receives the same type you would declare for a Pydantic model attribute, so, it can be a Pydantic model,
but it can also be, e.g. a list of Pydantic models, like List[Item]

FastAPI will use this response_model to:

Convert the output data to its type declaration.
Validate the data.
Add a JSON Schema for the response, in the OpenAPI path operation.
Will be used by the automatic documentation systems.
AND Will limit the output data to that of the model. We'll see how that's important below. !!!!!
"""
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []


@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item


# declaring a UserIn model, it will contain a plaintext password
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


# Add an output model
class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


# Don't do this in production!
@app.post("/user/", response_model=UserIn)
async def create_user(user: UserIn):
    return user
