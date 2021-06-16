"""
Response Status Code
status_code can alternatively also receive an IntEnum, such as Python's http.HTTPStatus

Return that status code in the response.
Document it as such in the OpenAPI schema (and so, in the user interfaces):
"""

from fastapi import FastAPI, status

app = FastAPI()


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
