"""Header Parameters
https://fastapi.tiangolo.com/tutorial/header-params/
You can define Header parameters the same way you define Query, Path and Cookie parameters.

Header has a little extra functionality on top of what Path, Query and Cookie provide.

Most of the standard headers are separated by a "hyphen" character, also known as the "minus symbol" (-).

But a variable like user-agent is invalid in Python.

So, by default, Header will convert the parameter names characters from underscore (_) to hyphen (-) to extract and
document the headers.


"""
from typing import Optional, List

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}


# If for some reason you need to disable automatic conversion of underscores to hyphens, set the parameter
# convert_underscores of Header to False:
# Before setting convert_underscores to False, bear in mind that some HTTP proxies and servers disallow the usage
# of headers with underscores.

@app.get("/items-without-convertion/")
async def read_items(
        strange_header: Optional[str] = Header(None, convert_underscores=False)
):
    return {"strange_header": strange_header}


# Duplicate headers
# It is possible to receive duplicate headers. That means, the same header with multiple values.
# You can define those cases using a list in the type declaration.
# You will receive all the values from the duplicate header as a Python list.

# to declare a header of X-Token that can appear more than once
@app.get("/items-with-multiple-x-token/")
async def read_items(x_token: Optional[List[str]] = Header(None)):
    """
    If you communicate with that path operation sending two HTTP headers like:

    X-Token: foo
    X-Token: bar
    The response would be like:


    {
        "X-Token values": [
            "bar",
            "foo"
        ]
    }
    OR
    {
    "X-Token values": [
        "string,string1"
        ]
    }
    """
    return {"X-Token values": x_token}
