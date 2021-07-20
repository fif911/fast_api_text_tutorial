from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

#  declare global dependencies that will be combined with the dependencies for each APIRouter:
app = FastAPI(dependencies=[Depends(get_query_token)])

# With app.include_router() we can add each APIRouter to the main FastAPI application.
# It will include all the routes from that router as part of it.
app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


# We can also add path operations directly to the FastAPI app.
@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
