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
