"""
Let's say you also have the endpoints dedicated to handling "items" from your application in the module at
app/routers/items.py.

!!!!!!!!!!!!!!!!
Tip

We can also add a list of tags and extra responses that will be applied to all the path operations included in this
router.
And we can add a list of dependencies that will be added to all the path operations in the router and will be
executed/solved for each request made to them.
!!!!!!!!!!!!!!!!!!
Note that, much like dependencies in path operation decorators, no value will be passed to your path operation function.

If you also declare dependencies in a specific path operation, they will be executed too.
The router dependencies are executed first, then the dependencies in the decorator, and then the normal parameter
dependencies.
You can also add Security dependencies with scopes.

Having dependencies in the APIRouter can be used, for example, to require authentication for a whole group of path
operations. Even if the dependencies are not added individually to each one of them.
"""
from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header

"""
We know all the path operations in this module have the same:

Path prefix: /items.
tags: (just one tag: items).
Extra responses.
dependencies: they all need that X-Token dependency we created.
So, instead of adding all that to each path operation, we can add it to the APIRouter."""
router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@router.get("/")
async def read_items():
    return fake_items_db


@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    """
We are not adding the prefix /items nor the tags=["items"] to each path operation because we added them to the APIRouter
But we can still add more tags that will be applied to a specific path operation, and also some extra responses specific
to that path operation

Tip
This last path operation will have the combination of tags: ["items", "custom"].
And it will also have both responses in the documentation, one for 404 and one for 403.
    """
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
