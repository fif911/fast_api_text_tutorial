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

Takeout:
Use the path operation decorator's parameter response_model to define response models and
especially to ensure private data is filtered out.

Use response_model_exclude_unset to return only the values explicitly set.
"""
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
    "baf": {
        "name": "Baf",
        "description": "There goes my baf",
        "price": 50.2,
        "tax": 10.5,
    },
}


# Your response model could have default values but you might want to omit them from the result if they were
# not actually stored For example, if you have models with many optional attributes in a NoSQL database, but
# you don't want to send very long JSON responses full of default values.
# Use the response_model_exclude_unset parameter
# and those default values won't be included in the response, only the values actually set.
@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    """
    FastAPI uses Pydantic model's .dict() with its exclude_unset parameter to achieve this.
    You can also use:

    response_model_exclude_defaults=True
    response_model_exclude_none=True

    as described in the Pydantic docs for exclude_defaults and exclude_none.

    even though description, tax, and tags have the same values as the defaults, they were set explicitly
    (instead of taken from the defaults) So, they will be included in the JSON response
    """
    return items[item_id]


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
    # required_test: str  # if returning field that doest exists - Internal server error


# Don't do this in production!
@app.post("/user/", response_model=UserOut)  # Fast API Will limit the output data with the specified model
async def create_user(user: UserIn):
    return user


# So, FastAPI will take care of filtering out all the data that is not declared in the output model (using Pydantic).


###############################################
"""
You can also use the path operation decorator parameters response_model_include and response_model_exclude.

They take a set of str with the name of the attributes to include (omitting the rest) or to exclude (including the rest)
But it is still recommended to use the ideas above, using multiple classes, instead of these parameters.
"""


@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
    # The syntax {"name", "description"} creates a set with those two values.
    # It is equivalent to set(["name", "description"]).
    # Using lists instead of sets
    # If you forget to use a set and use a list or tuple
    # response_model_include=["name", "description"],
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Item,
         response_model_exclude={"tax"})  # response_model_exclude=["tax"]
async def read_item_public_data(item_id: str):
    return items[item_id]
