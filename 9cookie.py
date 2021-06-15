"""
Cookie Parameters

You can define Cookie parameters the same way you define Query and Path parameters.
Cookie is a "sister" class of Path and Query. It also inherits from the same common Param class.

But remember that when you import Query, Path, Cookie and others from fastapi, those are actually
functions that return special classes.

To declare cookies, you need to use Cookie, because otherwise the parameters would be interpreted as query parameters.
"""

from typing import Optional

from fastapi import Cookie, FastAPI, Response

app = FastAPI()


# not working :
# curl -X 'GET' 'http://127.0.0.1:8000/items/' -H 'accept: application/json'  -H 'Cookie: ads_id=asdasd'
# working :
# curl -X GET "http://127.0.0.1:8000/items/" -H  "accept: application/json" -H  "Cookie: ads_id=foobar"

@app.get("/items/")
async def read_items(ads_id: Optional[str] = Cookie(None)):
    if ads_id:
        answer = "set to %s" % ads_id
    else:
        answer = "not set"
    return {"ads_id": answer}


@app.post("/cookie-and-object/")
def create_cookie(response: Response):
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {"message": "Come to the dark side, we have cookies"}
