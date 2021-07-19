"""
OAuth2 with Password (and hashing), Bearer with JWT tokens
JWT tech details in the bottom
https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#technical-details-about-the-jwt-subject-sub



Now that we have all the security flow, let's make the application actually secure, using JWT tokens and secure password hashing.
This code is something you can actually use in your application, save the password hashes in your database, etc.

About JWT¶
JWT means "JSON Web Tokens".

It is not encrypted, so, anyone could recover the information from the contents.
But it's signed. So, when you receive a token that you emitted, you can verify that you actually emitted it.
That way, you can create a token with an expiration of, let's say, 1 week. And then when the user comes back the next
day with the token, you know that user is still logged in to your system.
After a week, the token will be expired and the user will not be authorized and will have to sign in again to get a new
token. And if the user (or a third party) tried to modify the token to change the expiration, you would be able to
discover it, because the signatures would not match.

If you want to play with JWT tokens and see how they work, check https://jwt.io.
pip install python-jose[cryptography]

Passlib¶
PassLib is a great Python package to handle password hashes.
It supports many secure hashing algorithms and utilities to work with them.

The recommended algorithm is "Bcrypt".
pip install passlib[bcrypt]

Handle JWT tokens¶
Import the modules installed.
Create a random secret key that will be used to sign the JWT tokens.
To generate a secure random secret key use the command:
openssl rand -hex 32
09d25e094faa6ca2556c818166b7a9563b93f7....
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


# create object of crypting
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


"""
Technical details about the JWT "subject" sub

The JWT specification says that there's a key sub, with the subject of the token.
It's optional to use it, but that's where you would put the user's identification, so we are using it here.
JWT might be used for other things apart from identifying a user and allowing them to perform operations directly on your API.
For example, you could identify a "car" or a "blog post".
Then you could add permissions about that entity, like "drive" (for the car) or "edit" (for the blog).
And then, you could give that JWT token to a user (or bot), and they could use it to perform those actions (drive the car, or edit the blog post) without even needing to have an account, just with the JWT token your API generated for that.
Using these ideas, JWT can be used for way more sophisticated scenarios.
In those cases, several of those entities could have the same ID, let's say foo (a user foo, a car foo, and a blog post foo).
So, to avoid ID collisions, when creating the JWT token for the user, you could prefix the value of the sub key, e.g. with username:. So, in this example, the value of sub could have been: username:johndoe.
The important thing to have in mind is that the sub key should have a unique identifier across the entire application, and it should be a string.

Advanced usage with scopes¶
OAuth2 has the notion of "scopes".
You can use them to add a specific set of permissions to a JWT token.
Then you can give this token to a user directly or a third party, to interact with your API with a set of restrictions.
You can learn how to use them and how they are integrated into FastAPI later in the Advanced User Guide.
"""
