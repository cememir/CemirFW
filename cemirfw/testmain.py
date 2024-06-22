# main.py
import json

from cemirfw import CemirFW

app = CemirFW()

@app.get('/hello')
@app.require_login
@app.rate_limit(5, 10)
def hello(handler):
    return {"message": "Hello, World!"}

@app.post('/data')
@app.require_login
@app.rate_limit(5, 10)
def data_handler(handler):
    content_length = int(handler.headers['Content-Length'])
    post_data = handler.rfile.read(content_length)
    data = json.loads(post_data)
    response = {"received": data}
    return response

@app.get('/new_endpoint')
@app.require_login
@app.rate_limit(5, 10)
def new_endpoint(handler):
    return {"message": "This is a new endpoint"}

if __name__ == "__main__":
    app.run_with_reload()
