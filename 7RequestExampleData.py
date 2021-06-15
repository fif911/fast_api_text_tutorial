"""
Declare Request Example Data
You can declare examples of the data your app can receive.
"""

from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    # Keep in mind that those extra arguments passed won't add any validation, only extra information,
    # for documentation purposes.
    name: str = Field(..., example="Foo")
    description: Optional[str] = Field(None, example="A very nice Item")
    price: float = Field(..., example=35.4)
    tax: Optional[float] = Field(None, example=3.2)

    # name: str
    # description: Optional[str] = None
    # price: float
    # tax: Optional[float] = None

    class Config:
        """
        You could use the same technique to extend the JSON Schema and add your own custom extra info.
        For example you could use it to add metadata for a frontend user interface, etc.
        """
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


@app.put("/items-with-in-function-example/{item_id}")
async def update_item(
        item_id: int,
        item: Item = Body(  # when there is no example in shema
            ...,
            example={
                "name": "Foo",
                "description": "A very nice ItemS",  # this will override config in schema
                "price": 35.4,
                "tax": 3.2,
            },
        ),
):
    results = {"item_id": item_id, "item": item}
    return results


"""
Body with multiple examples
The keys of the dict identify each example, and each value is another dict.

Each specific example dict in the examples can contain:

summary: Short description for the example.
description: A long description that can contain Markdown text.
value: This is the actual example shown, e.g. a dict.
externalValue: alternative to value, a URL pointing to the example. Although this might not be supported by as many
tools as value.
"""


@app.put("/items-big-example/{item_id}")
async def update_item(
        *,
        item_id: int,
        item: Item = Body(
            ...,
            examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                },
            },
        ),
):
    results = {"item_id": item_id, "item": item}
    return results
