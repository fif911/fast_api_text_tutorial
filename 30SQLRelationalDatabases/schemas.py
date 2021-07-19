"""File with serializers"""
"""
WHAT DOES ORM_MODE = True means
Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any
other arbitrary object with attributes).

This way, instead of only trying to get the id value from a dict, as in:
id = data["id"]
it will also try to get it from an attribute, as in:
id = data.id

And with this, the Pydantic model is compatible with ORMs, and you can just declare it in the response_model argument
in your path operations.
You will be able to return a database model and it will read the data from it.

----
SQLAlchemy and many others are by default "lazy loading".
That means, for example, that they don't fetch the data for relationships from the database unless you try to access
the attribute that would contain that data.
For example, accessing the attribute items:
current_user.items
would make SQLAlchemy go to the items table and get the items for this user, but not before.
Without orm_mode, if you returned a SQLAlchemy model from your path operation, it wouldn't include the relationship data

Even if you declared those relationships in your Pydantic models.
But with ORM mode, as Pydantic itself will try to access the data it needs from attributes (instead of assuming a dict),
you can declare the specific data you want to return and it will be able to go and get it, even from ORMs.
"""
from typing import List, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
