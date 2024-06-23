# CemirFW

CemirFW is a lightweight framework for building REST APIs using Tornado. It provides decorators to register routes for different HTTP methods (GET, POST, PUT, DELETE) and handles HTTP requests accordingly.

## Version
Current Version: 1.0.1

## Features
- Register routes with decorators (`get`, `post`, `put`, `delete`).
- Parse request data including JSON bodies and query parameters.
- Custom logging of HTTP request details based on response status codes.

## Getting Started
To use CemirFW, follow these steps:

1. Install the required dependencies (Tornado).
2. Define your routes using the `get`, `post`, `put`, `delete` decorators provided by `CemirFW`.
3. Implement your request handlers with asynchronous methods to process incoming requests.
4. Instantiate an instance of `CemirFW`, configure your host and port, and call the `run` method to start the server.

```python
from cemirfw import fw



@fw.get("/user")
async def get_users(handler):
    return [{"user_id": 1}, {"user_id": 3}]


@fw.get("/user/{user_id}")
async def get_user(handler, user_id):
    user_agent = handler.request.headers.get('User-Agent', 'Unknown')
    return {"user_id": user_id, "user_agent": user_agent}


@fw.post("/user")
async def create_user(handler):
    body = handler.body
    return {"message": "User created successfully", "data": body}, 201


@fw.put("/user/{user_id}")
async def update_user(handler, user_id):
    body = handler.body
    return {"message": f"User {user_id} updated", "data": body}


@fw.delete("/user/{user_id}")
async def delete_user(handler, user_id):
    return {"message": f"User {user_id} deleted"}


fw.host = "0.0.0.0"
fw.port = 8001

fw.run()

```