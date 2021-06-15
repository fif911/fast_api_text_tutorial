"""
Body - Multiple Parameters
you can mix Path, Query and request body parameter declarations freely and FastAPI will know what to do.
"""

# mix Path, Query and request body parameter declarations
from typing import Optional

from fastapi import FastAPI, Path, Body
from pydantic import BaseModel

from serializers import Item, User

app = FastAPI()


@app.put("/items/{item_id}")
async def update_item(
        *,
        item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),  # path param
        q: Optional[str] = None,  # query param
        item: Optional[Item] = None,  # body param Only cause it's Pydantic model !
):
    """
    Notice that, in this case, the item that would be taken from the body is optional. As it has a None default value.
    """
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


@app.put("/items-with-user/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    """
    In this case, FastAPI will notice that there are more than one body parameters in the function
    (two parameters that are Pydantic models).

    So, it will then use the parameter names as keys (field names) in the body, and expect a body like:
    {
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
        },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
        }
    }
    """
    results = {"item_id": item_id, "item": item, "user": user}
    return results


# to set Single value in body and not in query user Body

@app.put("/items-single-mandatory/{item_id}")
async def update_item(
        item_id: int, item: Item, user: User, importance: int = Body(..., gt=0)  # Body mandatory
        # item_id: int, item: Item, user: User, importance: int = Body(None) $ body optional
):
    # Fast API will expect body with 2 embed dict keys item, user and 1 param importance
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


@app.put("/items-single-mandatory-and-query/{item_id}")
async def update_item(
        *,
        item_id: int,
        item: Item,
        user: User,
        importance: int = Body(..., gt=0),
        q: Optional[str] = None
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results


# Embed a single body parameter
# But if you want it to expect a JSON with a key item and inside of it the model contents, as it does when you
# declare extra body parameters, you can use the special Body parameter embed:
# item: Item = Body(..., embed=True)

@app.put("/items-embed/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    """
    In this case FastAPI will expect a body like:
    (you can instruct FastAPI to embed the body in a key even when there is only a single parameter declared.)
    
    {
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
    }
instead of:
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
    """
    return results
