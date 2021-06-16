"""
Path Operation Configuration
"""

from typing import Optional, Set

from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []


@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["items"],
          summary="Create an item",
          description="Create an item with all the information, name, description, price, tax and a set of unique tags",
          response_description="The created item",  # response_description refers specifically to the response
          )
async def create_item(item: Item):
    return item


@app.get("/items/", tags=["items"])
async def read_items():
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    \f THIS IS DESCRIPTION FROM DOC STRING
    """
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=["users"], deprecated=True, )
async def read_users():
    return [{"username": "johndoe"}]
