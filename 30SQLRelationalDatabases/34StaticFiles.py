"""
You can serve static files automatically from a directory using StaticFiles.

Use StaticFiles¶
Import StaticFiles.
"Mount" a StaticFiles() instance in a specific path.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

"""
What is "Mounting"¶
"Mounting" means adding a complete "independent" application in a specific path, that then takes care of handling all
the sub-paths.

This is different from using an APIRouter as a mounted application is completely independent. The OpenAPI and docs from
your main application won't include anything from the mounted application, etc.

The first "/static" refers to the sub-path this "sub-application" will be "mounted" on. So, any path that starts with
"/static" will be handled by it.
The directory="static" refers to the name of the directory that contains your static files.
The name="static" gives it a name that can be used internally by FastAPI.
All these parameters can be different than "static", adjust them with the needs and specific details of your own
application.
"""