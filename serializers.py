from typing import Optional

from pydantic import BaseModel


class Item(BaseModel):
    """
    The same as when declaring query parameters, when a model attribute has a default value, it is not required.
    Otherwise, it is required. Use None to make it just optional.
    """
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class User(BaseModel):
    username: str
    full_name: Optional[str] = None

# class Item(BaseModel):
#     # Field works the same way as Query, Path and Body, it has all the same parameters, etc.
#     name: str
#     description: Optional[str] = Field(
#         None, title="The description of the item", max_length=300
#     )
#     price: float = Field(..., gt=0, description="The price must be greater than zero")
#     tax: Optional[float] = None
