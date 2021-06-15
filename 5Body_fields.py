from typing import Optional

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

"""
Notice that Field is imported directly from pydantic, not from fastapi as are all the rest (Query, Path, Body, etc).
"""
app = FastAPI()


class Item(BaseModel):
    # Field works the same way as Query, Path and Body, it has all the same parameters, etc.
    name: str
    description: Optional[str] = Field(
        None, title="The description of the item", max_length=300
    )
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: Optional[float] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
