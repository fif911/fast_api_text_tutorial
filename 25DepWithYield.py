"""
                                                # Dependencies with yield
FastAPI supports dependencies that do some extra steps after finishing.

To do this, use yield instead of return, and write the extra steps after.
(Make sure to use yield one single time.)
                        (Any function that is valid to use with:

                        @contextlib.contextmanager or
                        @contextlib.asynccontextmanager
                        would be valid to use as a FastAPI dependency.

                        In fact, FastAPI uses those two decorators internally.)
"""
from fastapi import Depends, File


class DBSession:
    def __init__(self):
        print("INIT")

    @classmethod
    def close(cls):
        print("CLOSED")


async def get_db():
    # Only the code prior to and including the yield statement is executed before sending a response
    db = DBSession()
    try:
        yield db  # The yielded value is what is injected into path operations and other dependencies:
    # The code following the yield statement is executed after the response has been delivered:
    finally:
        db.close()


"""
A dependency with yield and try
If you use a try block in a dependency with yield, you'll receive any exception that was thrown when using the dependenc
For example, if some code at some point in the middle, in another dependency or in a path operation,
made a database transaction "rollback" or create any other error, you will receive the exception in your dependency.

So, you can look for that specific exception inside the dependency with except SomeException.

In the same way, you can use finally to make sure the exit steps are executed, no matter if there was an exception
or not.
"""

"""
Sub-dependencies with yield
You can have sub-dependencies and "trees" of sub-dependencies of any size and shape, and any or all of them can use
yield.
For example, dependency_c can have a dependency on dependency_b, and dependency_b on dependency_a:
"""


async def dependency_a():
    dep_a = "generate_dep_a"
    try:
        yield dep_a
    finally:
        dep_a.close()


async def dependency_b(dep_a=Depends(dependency_a)):
    dep_b = "generate_dep_b()"
    try:
        yield dep_b
    finally:
        dep_b.close(dep_a)


async def dependency_c(dep_b=Depends(dependency_b)):
    dep_c = "generate_dep_c()"
    try:
        yield dep_c
    finally:
        dep_c.close(dep_b)


"""
The same way, you could have dependencies with yield and return mixed.

And you could have a single dependency that requires several other dependencies with yield, etc.

# Dependencies with yield and HTTPException
You can still raise exceptions including HTTPException before the yield. But not after.
https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#dependencies-with-yield-and-httpexception

# Context Managers¶
What are "Context Managers"¶
"Context Managers" are any of those Python objects that you can use in a with statement.

In Python, you can create Context Managers by creating a class with two methods: __enter__() and __exit__().

You can also use them inside of FastAPI dependencies with yield by using with or async with statements inside
of the dependency function:
"""


class MySuperContextManager:
    def __init__(self):
        self.db = DBSession()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


async def get_db():
    with MySuperContextManager() as db:
        yield db
