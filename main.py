from fastapi import FastAPI

app = FastAPI()  # FastAPI is a class that inherits directly from Starlette.

"""Path" here refers to the last part of the URL starting from the first /
A "path" is also commonly called an "endpoint" or a "route".
So, in a URL like: https://example.com/items/foo
...the path would be: /items/foo
"""


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}
