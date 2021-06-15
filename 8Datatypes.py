"""
Extra Data Types
int
float
str
bool

UUID
In requests and responses will be represented as a str.

datetime.datetime:
A Python datetime.datetime.
In requests and responses will be represented as a str in ISO 8601 format, like: 2008-09-15T15:53:00+05:00.

datetime.date:
Python datetime.date.
In requests and responses will be represented as a str in ISO 8601 format, like: 2008-09-15

datetime.time:
A Python datetime.time.
In requests and responses will be represented as a str in ISO 8601 format, like: 14:23:55.003

datetime.timedelta:
A Python datetime.timedelta.
In requests and responses will be represented as a float of total seconds.

frozenset:
In requests and responses, treated the same as a set:
In requests, a list will be read, eliminating duplicates and converting it to a set.
In responses, the set will be converted to a list.
The generated schema will specify that the set values are unique (using JSON Schema's uniqueItems).

bytes:
Standard Python bytes.
In requests and responses will be treated as str.
The generated schema will specify that it's a str with binary "format".

Decimal:
Standard Python Decimal.
In requests and responses, handled the same as a float.

You can check all the valid pydantic data types here: Pydantic data types.
https://pydantic-docs.helpmanual.io/usage/types/
"""
from datetime import datetime, time, timedelta
from typing import Optional
from uuid import UUID

from fastapi import Body, FastAPI

app = FastAPI()


@app.put("/items/{item_id}")
async def read_items(
        item_id: UUID = None,
        start_datetime: Optional[datetime] = Body(None),
        end_datetime: Optional[datetime] = Body(None),
        repeat_at: Optional[time] = Body(None),
        process_after: Optional[timedelta] = Body(None),
):
    # Note that the parameters inside the function have their natural data type, and you can, for example,
    # perform normal date manipulations, like:
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }
