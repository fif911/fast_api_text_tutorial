"""
You can define background tasks to be run after returning a response.
This is useful for operations that need to happen after a request, but that the client doesn't really have to be waiting
 for the operation to complete before receiving the response.
This includes, for example:

Email notifications sent after performing an action:

As connecting to an email server and sending an email tends to be "slow" (several seconds), you can return the response
right away and send the email notification in the background.

Processing data:
For example, let's say you receive a file that must go through a slow process, you can return a response of "Accepted"
(HTTP 202) and process it in the background.
"""

from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    # import BackgroundTasks and define a parameter in your path operation function with a type declaration of
    # BackgroundTasks:
    #
    # .add_task() receives as arguments:
    # A task function to be run in the background (write_notification).
    # Any sequence of arguments that should be passed to the task function in order (email).
    # Any keyword arguments that should be passed to the task function (message="some notification").
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}


"""
Dependency Injection
Using BackgroundTasks also works with the dependency injection system, you can declare a parameter of type
BackgroundTasks at multiple levels: in a path operation function, in a dependency (dependable), in a sub-dependency, etc

In this example, the messages will be written to the log.txt file after the response is sent.
If there was a query in the request, it will be written to the log in a background task.
And then another background task generated at the path operation function will write a message using the email path
parameter.
"""

from typing import Optional

from fastapi import BackgroundTasks, Depends, FastAPI

app = FastAPI()


def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: Optional[str] = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q


@app.post("/send-notification/{email}")
async def send_notification(
        email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}
