"""
It is based on Requests, so it's very familiar and intuitive.
With it, you can use pytest directly with FastAPI.

Using TestClient:
Create functions with a name that starts with test_ (this is standard pytest conventions).
Use the TestClient object the same way as you do with requests.
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)


def test_read_main():
    """
    Notice that the testing functions are normal def, not async def.
    And the calls to the client are also normal calls, not using await.
    This allows you to use pytest directly without complications.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
