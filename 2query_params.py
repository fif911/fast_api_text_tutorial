"""Query Parameters and String Validations"""
from typing import Optional, List

from fastapi import FastAPI, Query

app = FastAPI()


# async def read_items(q: Optional[str] = None):
# Additional validation
@app.get("/items/")
async def read_items(q: Optional[str] = Query(None, max_length=50, min_length=3)):
    """
    FastAPI will know that the value of q is not required because of the default value = None.

    The Optional in Optional[str] is not used by FastAPI, but will allow your editor to give you better support
    and detect errors.

    We are going to enforce that even though q is optional, whenever it is provided, its length doesn't
    exceed 50 characters.

    So:
q: Optional[str] = Query(None)
...makes the parameter optional, the same as:
q: Optional[str] = None
But it declares it explicitly as being a query parameter.
    """
    # FastAPI allows you to declare additional information and validation for your parameters.
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


"""
min/max length
q: Optional[str] = Query(None, min_length=3, max_length=50)
also the regular exp:
q: Optional[str] = Query(None, min_length=3, max_length=50, regex="^fixedquery$")
Default values: NOTE (Having a default value makes the parameter optional.)
q: str = Query("fixedquery", min_length=3)

Make it required
When we don't need to declare more validations or metadata, we can make the q query parameter required just
by not declaring a default value, like:
q: str 

So, when you need to declare a value as required while using Query, you can use ... as the first argument:
q: str = Query(..., min_length=3)
If you hadn't seen that ... before: it is a special single value, it is part of Python and is called "Ellipsis"
This will let FastAPI know that this parameter is required.





Query parameter list / multiple values
When you define a query parameter explicitly with Query you can also declare it to receive a list of values,
or said in other way, to receive multiple values.
q that can appear multiple times in the URL, you can write:
"""


# /list-items/?q=1&q=2&q=3&q=string&q=string
@app.get("/list-items/")
async def read_items(q: List[str] = Query(["foo", "bar"])):
    """
    \f
    To declare a query parameter with a type of list, like in the example above, you need to explicitly
    use Query, otherwise it would be interpreted as a request body.
    also we can provide defaults:
    async def read_items(q: List[str] = Query(["foo", "bar"])):

    or optional fields
    q: Optional[List[str]] = Query(None)


You can also use list directly instead of List[str]:
q: list = Query([])
    Have in mind that in this case, FastAPI won't check the contents of the list.
For example, List[int] would check (and document) that the contents of the list are integers. But list alone wouldn't.
    """
    query_items = {"q": q}
    returns = {
        "q": [
            "foo",
            "bar"
        ]
    }
    return query_items


# Declare more metadata
@app.get("/more-mt-list-items/")
async def read_items(
        q: Optional[str] = Query(
            None,  # means that optional for Fast API.  Optional[str] means optional for pycharm
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
        )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


"""
# Alias parameters

Imagine that you want the parameter to be item-query.

Like in:


http://127.0.0.1:8000/items/?item-query=foobaritems
But item-query is not a valid Python variable name.

The closest would be item_query.

But you still need it to be exactly item-query
Then you can declare an alias, and that alias is what will be used to find the parameter value:"""


@app.get("/alias-items/")
async def read_items(q: Optional[str] = Query(None, alias="item-query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


"""
Deprecating parameter
Now let's say you don't like this parameter anymore.

You have to leave it there a while because there are clients using it, but you want the docs to clearly show it as deprecated.

Then pass the parameter deprecated=True to Query:
"""


@app.get("/deprecated-items/")
async def read_items(
        q: Optional[str] = Query(
            None,
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            regex="^fixedquery$",
            deprecated=True,
        )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
