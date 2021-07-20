"""" Bigger Applications - Multiple File """

"""
FastAPI provides a convenience tool to structure your application while keeping all the flexibility.
(If you come from Flask, this would be the equivalent of Flask's Blueprints)

An example file structure¶
Let's say you have a file structure like this:
├── app                  # "app" is a Python package
│   ├── __init__.py      # this file makes "app" a "Python package"
│   ├── main.py          # "main" module, e.g. import app.main
│   ├── dependencies.py  # "dependencies" module, e.g. import app.dependencies
│   └── routers          # "routers" is a "Python subpackage"
│   │   ├── __init__.py  # makes "routers" a "Python subpackage"
│   │   ├── items.py     # "items" submodule, e.g. import app.routers.items
│   │   └── users.py     # "users" submodule, e.g. import app.routers.users
│   └── internal         # "internal" is a "Python subpackage"
│       ├── __init__.py  # makes "internal" a "Python subpackage"
│       └── admin.py     # "admin" submodule, e.g. import app.internal.admin
"""

"""
APIRouter
 the file dedicated to handling just users is the submodule at /app/routers/users.py
 You want to have the path operations related to your users separated from the rest of the code, to keep it organized.
 You can create the path operations for that module using APIRouter.
 
You can think of APIRouter as a "mini FastAPI" class.
All the same options are supported.
All the same parameters, responses, dependencies, tags, etc.



You can also use .include_router() multiple times with the same router using different prefixes.
This could be useful, for example, to expose the same API under different prefixes, e.g. /api/v1 and /api/latest.

The same way you can include an APIRouter in a FastAPI application, you can include an APIRouter in another APIRouter using:
router.include_router(other_router)
(Make sure you do it before including router in the FastAPI app, so that the path operations from other_router
are also included.)
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
