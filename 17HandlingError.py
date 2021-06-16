"""
Use HTTPException

# SUPER USEFUL WHILE DEBUGGING & DEVELOPING THING
#  https://fastapi.tiangolo.com/tutorial/handling-errors/#use-the-requestvalidationerror-body

Also we can Re-use FastAPI's exception handlers for debugging
https://fastapi.tiangolo.com/tutorial/handling-errors/#re-use-fastapis-exception-handlers

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)
"""
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException
# You could also use from starlette.requests import Request and from starlette.responses import JSONResponse.
from starlette import status
from starlette.responses import PlainTextResponse

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    """\f
    When raising an HTTPException, you can pass any value that can be converted to JSON as the parameter detail,
    not only str.
    You could pass a dict, a list, etc.

    They are handled automatically by FastAPI and converted to JSON.
    """
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail=["Item not found", "bla :)"],
            headers={"X-Error": "There goes my error"},  # Add custom headers
        )
        # raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}


# Install custom exception handlers
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


# Override the default exception handlers
# Override request validation exceptions

# Custom HTTPException Error
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


# Custom Validation Error
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     return PlainTextResponse(str(exc), status_code=400)


# http://127.0.0.1:8000/items-exception/asd - follow to see custom HTTP exception
@app.get("/items-exception/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}


class Item(BaseModel):
    title: str
    size: int


# SUPER USEFUL WHILE DEBUGGING THING
#  https://fastapi.tiangolo.com/tutorial/handling-errors/#use-the-requestvalidationerror-body
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.post("/items/")
async def create_item(item: Item):
    return item
