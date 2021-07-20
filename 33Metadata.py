"""
Metadata and Docs URLs
You can customize several metadata configurations in your FastAPI application.
"""

from fastapi import FastAPI

# app = FastAPI(
#     title="My Super Project",
#     description="This is a very fancy project, with auto docs for the API and everything",
#     version="2.5.0",
# )
#
# Order of tags¶
# The order of each tag metadata dictionary also defines the order shown in the docs UI.
# For example, even though users would go after items in alphabetical order, it is shown before them,
# because we added their metadata as the first dictionary in the
tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]
# By default, the OpenAPI schema is served at /openapi.json.
# But you can configure it with the parameter openapi_url.
app = FastAPI(openapi_tags=tags_metadata, openapi_url="/api/v1/openapi.json")
# If you want to disable the OpenAPI schema completely you can set openapi_url=None, that will also disable the
# documentation user interfaces that use it.

"""
You can configure the two documentation user interfaces included:

Swagger UI: served at /docs.
You can set its URL with the parameter docs_url.
You can disable it by setting docs_url=None.
ReDoc: served at /redoc.
You can set its URL with the parameter redoc_url.
You can disable it by setting redoc_url=None.
For example, to set Swagger UI to be served at /documentation and disable ReDoc:

        FastAPI(docs_url="/documentation", redoc_url=None)
"""


@app.get("/users/", tags=["users"])
async def get_users():
    return [{"name": "Harry"}, {"name": "Ron"}]


@app.get("/items/", tags=["items"])
async def get_items():
    return [{"name": "wand"}, {"name": "flying broom"}]


# @app.get("/items/")
# async def read_items():
#     return [{"name": "Foo"}]

"""Metadata for tags
Each dictionary can contain:

name (required): a str with the same tag name you use in the tags parameter in your path operations and APIRouters.
description: a str with a short description for the tag. It can have Markdown and will be shown in the docs UI.
externalDocs: a dict describing external documentation with:
    description: a str with a short description for the external docs.
    url (required): a str with the URL for the external documentation.
"""
