from enum import Enum
from typing import Optional

from fastapi import FastAPI

# uvicorn main:app --reload to start the server
from serializers import Item

app = FastAPI()  # FastAPI is a class that inherits directly from Starlette.

"""Path" here refers to the last part of the URL starting from the first /
A "path" is also commonly called an "endpoint" or a "route".
So, in a URL like: https://example.com/items/foo
...the path would be: /items/foo
"""


@app.get("/")
async def root():
    return {"message": "Hello World"}


# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     """
#     The value of the path parameter item_id will be passed to your function as the argument item_id.
#     You can declare the type of a path parameter in the function, using standard Python type annotations
#     This will give you editor support inside of your function, with error checks, completion, etc.
#     Notice that the value your function received (and returned) is 3, as a Python int, not a string "3".
#
#     So, with that type declaration, FastAPI gives you automatic request "parsing".
#
#     All the data validation is performed under the hood by Pydantic, so you get all the benefits from it.
#     """
#     return {"item_id": item_id}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


# Create an Enum class
class ModelName(str, Enum):
    """
    By inheriting from str the API docs will be able to know that the values
    must be of type string and will be able to render correctly.
    """
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


"""
Query Parameters
When you declare other function parameters that are not part of the path parameters, they are automatically
interpreted as "query" parameters.

http://127.0.0.1:8000/items/?skip=0&limit=10
http://127.0.0.1:8000/items/?skip=20 only overrides skip

As query parameters are not a fixed part of a path, they can be optional and can have default values.
"""
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


# Optional parameters
# # async def read_item(item_id: str, q: Optional[str] = None)
# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
#     """
#     In this case, the function parameter q will be optional, and will be None by default.
#     FastAPI is smart enough to notice that the path parameter item_id is a path parameter and q is not,
#     so, it's a query parameter.
#
#     FastAPI will know that q is optional because of the = None.
#
#     The Optional in Optional[str] is not used by FastAPI (FastAPI will only use the str part),
#     but the Optional[str] will let your editor help you finding errors in your code.
#     """
#     # if q:
#     #     return {"item_id": item_id, "q": q}
#     # return {"item_id": item_id}
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item


# Multiple path and query parameters. They will be detected by name:
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
        user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# Required query parameters


@app.get("/items/{item_id}")
async def read_user_item(
        # item_id: str, needy: str
        item_id: str, needy: str, skip: int = 0, limit: Optional[int] = None
):
    """
    when you want to make a query parameter required, you can just not declare any default value

    In this case, there are 3 query parameters:

        needy, a required str.
        skip, an int with a default value of 0.
        limit, an optional int.

    You could also use Enums the same way as with Path Parameters
    """
    # item = {"item_id": item_id, "needy": needy}
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item


# Request Body


# @app.post("/items/")
# async def create_item(item: Item):
#     """
#     Declare model as a parameter
#     """
#     return item

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# Request body + path parameters
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    """
    FastAPI will recognize that the function parameters that match path parameters should be taken from the path,
    and that function parameters that are declared to be Pydantic models should be taken from the request body.
    """
    return {"item_id": item_id, **item.dict()}


"""
item_id: str, needy: str, skip: int = 0, limit: Optional[int] = None

If None - not required (optional)     e.g.   q: Optional[str] = None  = q: Optional[str] = Query(None, min_length=3)
if = value - default value so not required (optional)  e.g. q:str = "alex" q: str = Query("fixedquery", min_length=3)
if req_val: str -  just declaration so required OR (q: str = Query(..., min_length=3)
 
"""
