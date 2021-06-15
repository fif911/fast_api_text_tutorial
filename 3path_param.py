"""
Path Parameters and Numeric Validations
The same way you can declare more validations and metadata for query parameters with Query, you can
declare the same type of validations and metadata for path parameters with Path.


"""

from typing import Optional

from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
        item_id: int = Path(..., title="The ID of the item to get"),  # A path parameter is always required
        q: Optional[str] = Query(None, alias="item-query"),
        # without using Query()  + q is required (ordering thing)
        # q: str, item_id: int = Path(..., title="The ID of the item to get")
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


"""
* explanation
Order the parameters as you need, tricks
If you want to declare the q query parameter without a Query nor any default value, and the path
parameter item_id using Path, and have them in a different order, Python has a little special syntax for that.

Pass *, as the first parameter of the function.

Python won't do anything with that *, but it will know that all the following parameters should be called as
keyword arguments (key-value pairs), also known as kwargs. Even if they don't have a default value.
(
*,
item_id: int = Path(..., title="The ID of the item to get"), 
q: str
):

Example
def bar(*, kwarg=None): 
    return kwarg
    

bar('kwarg') - ERROR
bar(kwarg='kwarg') - WORKING

"""


@app.get("/items/{item_id}")
async def read_items(
        *, item_id: int = Path(..., title="The ID of the item to get"), q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


"""
Number validations: greater/less than or equal

gt: greater than
ge: greater than or equal
lt: less than
le: less than or equal
"""


@app.get("/number-validation-items/{item_id}")
async def read_items(
        *,
        item_id: int = Path(..., title="The ID of the item to get", gt=0, le=1000),
        q: str,
        size: float = Query(..., gt=0, lt=10.5),  # float validation
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


"""
Query, Path, and others you will see later are subclasses of a common Param class (that you don't need to use).

When you import Query, Path and others from fastapi, they are actually functions.

That when called, return instances of classes of the same name.

So, you import Query, which is a function. And when you call it, it returns an instance of a class also named Query.

These functions are there (instead of just using the classes directly) so that your editor doesn't mark errors about
their types.

That way you can use your normal editor and coding tools without having to add custom configurations to disregard
those errors.
"""
