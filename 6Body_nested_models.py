"""
Body - Nested Models
With FastAPI, you can define, validate, document, and use arbitrarily deeply nested models (thanks to Pydantic).
"""

from typing import Optional, List, Set, Dict

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


# https://pydantic-docs.helpmanual.io/usage/types/
# Nested Model
class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    # tags: list = []  # an attribute as a subtype. Now the type of objects in list is not declared
    # tags: List[str] = []  # list of strings
    tags: Set[str] = set()  # set of strings (list of unique strings)
    """
    With this, even if you receive a request with duplicate data, it will be converted to a set of unique items.
    And whenever you output that data, even if the source had duplicates, it will be output as a set of unique items.
    """
    # image: Optional[Image] = None  # nested model (Use the submodel as a type)
    images: Optional[List[Image]] = None  # list of nested models


# Deeply nested models
class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    items: List[Item]


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


@app.post("/offers/")
async def create_offer(offer: Offer):
    # Notice how Offer has a list of Items, which in turn have an optional list of Images
    return offer


# Bodies of pure lists
@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
    return images


# In this case, you would accept any dict as long as it has int keys with float values:
@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    """
    Have in mind that JSON only supports str as keys.

    But Pydantic has automatic data conversion.
    This means that, even though your API clients can only send strings as keys, as long as those strings contain
    pure integers, Pydantic will convert them and validate them.
    """
    return weights
