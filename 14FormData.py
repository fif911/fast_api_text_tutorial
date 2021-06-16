"""
Form Data
When you need to receive form fields instead of JSON, you can use Form

With Form you can declare the same metadata and validation as with Body (and Query, Path, Cookie).
"""
from fastapi import FastAPI, Form

app = FastAPI()


@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}
