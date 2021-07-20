"""Now, let's imagine your organization gave you the app/internal/admin.py file.

It contains an APIRouter with some admin path operations that your organization shares between several projects.

For this example it will be super simple. But let's say that because it is shared with other projects in the
organization, we cannot modify it and add a prefix, dependencies, tags, etc. directly to the APIRouter:

We can declare all that without having to modify the original APIRouter by passing those parameters to
app.include_router() in main.py:

But that will only affect that APIRouter in our app, not in any other code that uses it.
So, for example, other projects could use the same APIRouter with a different authentication method.
"""
from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}