"""
ctrl+shift+f search in all files
ctrl + e open recent
ctrl +t merge from master
shift + shift search modules (function/classes/vars)
ctrl + j - completion for default constructions
ctrl + f12 - file structure

Sub-dependencies
You can create dependencies that have sub-dependencies.
They can be as deep as you need them to be.
FastAPI will take care of solving them.
"""

from typing import Optional

from fastapi import Cookie, Depends, FastAPI

app = FastAPI()


# First dependency "dependable. THis will be run first
def query_extractor(q: Optional[str] = None):
    return q


async def needy_dependency(fresh_value: str = Depends(query_extractor, use_cache=False)):
    """
    # Using the same dependency multiple times

    If one of your dependencies is declared multiple times for the same path operation, for example, multiple dependencies
    have a common sub-dependency, FastAPI will know to call that sub-dependency only once per request.

    And it will save the returned value in a "cache" and pass it to all the "dependants" that need it in that specific
    request, instead of calling the dependency multiple times for the same request.

    In an advanced scenario where you know you need the dependency to be called at every step (possibly multiple times)
    in the same request instead of using the "cached" value, you can set the parameter use_cache=False when using Depends:
    """
    return {"fresh_value": fresh_value}


# this will be runs second
def query_or_cookie_extractor(
        q: str = Depends(query_extractor), last_query: Optional[str] = Cookie(None)
):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    # and this will be run third
    return {"q_or_cookie": query_or_default}
