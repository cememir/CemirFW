import requests
import json

url = 'http://localhost:8000/data'
headers = {
    'Authorization': 'valid_token',  # Giriş gerekliliği için gerekli
    'Content-Type': 'application/json'
}
data = {
    'key1': 'value1',
    'key2': 'value2'
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print('Status Code:', response.status_code)
print('Response JSON:', response.json())
