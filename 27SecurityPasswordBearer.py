"""
Simple OAuth2 with Password and Beare

OAuth2PasswordRequestForm is a class dependency that declares a form body with:

The username.
The password.
An optional scope field as a big string, composed of strings separated by spaces.
An optional grant_type.

The OAuth2 spec actually requires a field grant_type with a fixed value of password, but OAuth2PasswordRequestForm
doesn't enforce it.

If you need to enforce it, use OAuth2PasswordRequestFormStrict instead of OAuth2PasswordRequestForm

scope¶
The spec also says that the client can send another form field "scope".
The form field name is scope (in singular), but it is actually a long string with "scopes" separated by spaces.
Each "scope" is just a string (without spaces).

An optional client_id (we don't need it for our example).
An optional client_secret (we don't need it for our example).

"Hashing" means: converting some content (a password in this case) into a sequence of bytes (just a string) that looks
like gibberish.
Whenever you pass exactly the same content (exactly the same password) you get exactly the same gibberish.
But you cannot convert from the gibberish back to the password.
"""
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="1Incorrect username or password")
    user = UserInDB(**user_dict)
    # Unwrapping. The same as:
    # UserInDB(
    #     username=user_dict["username"],
    #     email=user_dict["email"],
    #     full_name=user_dict["full_name"],
    #     disabled=user_dict["disabled"],
    #     hashed_password=user_dict["hashed_password"],
    # )

    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="2Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me",response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user