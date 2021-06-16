"""
Let's imagine that you have a database fake_db that only receives JSON compatible data.
For example, it doesn't receive datetime objects, as those are not compatible with JSON.
So, a datetime object would have to be converted to a str containing the data in ISO format.
The same way, this database wouldn't receive a Pydantic model (an object with attributes), only a dict.
You can use jsonable_encoder for that.

In this example, it would convert the Pydantic model to a dict, and the datetime to a str.
"""

from datetime import datetime
from typing import Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Optional[str] = None


app = FastAPI()


# receives the JSON compatible string == datetime
@app.put("/items/{id}")
def update_item(id: str, item: Item):
    # here it's already converted with pydantic to python datetime
    print(item.timestamp)
    # here we converting it again to json
    json_compatible_item_data = jsonable_encoder(item)
    print(json_compatible_item_data)
    fake_db[id] = json_compatible_item_data
