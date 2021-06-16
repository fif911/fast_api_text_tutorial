"""
Dependencies - First Steps
FastAPI has a very powerful but intuitive Dependency Injection system.

"Dependency Injection" means, in programming, that there is a way for your code (in this case, your path operation
functions) to declare things that it requires to work and use: "dependencies".

And then, that system (in this case FastAPI) will take care of doing whatever is needed to provide your code
with those needed dependencies ("inject" the dependencies).

This is very useful when you need to:

Have shared logic (the same code logic again and again).
Share database connections.
Enforce security, authentication, role requirements, etc.
And many other things...
All these, while minimizing code repetition.

You only give Depends a single parameter.

This parameter must be something like a function.

Whenever a new request arrives, FastAPI will take care of:

Calling your dependency ("dependable") function with the correct parameters.
Get the result from your function.
Assign that result to the parameter in your path operation function.

    # SHORTCUT
    # commons: CommonQueryParams = Depends(CommonQueryParams)
    # THE SAME AS:
    # commons: CommonQueryParams = Depends()

"""

from typing import Optional

from fastapi import Depends, FastAPI

app = FastAPI()


# It is just a function that can take all the same parameters that a path operation function can take:
async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons


# Classes as dependencies
# We do it for editor support
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items-class-depended/")
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    # SHORTCUT
    # commons: CommonQueryParams = Depends(CommonQueryParams)
    # THE SAME AS:
    # commons: CommonQueryParams = Depends()
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip: commons.skip + commons.limit]
    response.update({"items": items})
    return response
