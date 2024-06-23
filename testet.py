import requests

response = requests.get('http://localhost:8080/user')
print(response.json())  # [{ "user_id": 1 }, { "user_id": 2 }]

response = requests.get('http://localhost:8080/user/1')
print(response.json())  # { "user_id": "1", "user_agent": "..." }

user_data = {
    "name": "John Doe",
    "email": "john.doe@example.com"
}

response = requests.post('http://localhost:8080/user', json=user_data)
print(response.json())  # { "message": "User created successfully", "data": { "name": "John Doe", "email": "john.doe@example.com" } }

updated_user_data = {
    "name": "Jane Doe",
    "email": "jane.doe@example.com"
}

response = requests.put('http://localhost:8080/user/1', json=updated_user_data)
print(response.json())  # { "message": "User 1 updated", "data": { "name": "Jane Doe", "email": "jane.doe@example.com" } }

response = requests.delete('http://localhost:8080/user/1')
print(response.json())  # { "message": "User 1 deleted" }
