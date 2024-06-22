# cemirfw.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time
import asyncio
import os
import sys
from functools import wraps

ver = "0.0.1"


class CemirFW:
    def __init__(self):
        self.routes = {}
        self.tokens = ["valid_token"]
        self.rate_limits = {}

    def route(self, path, method):
        def decorator(func):
            if path not in self.routes:
                self.routes[path] = {}
            self.routes[path][method] = func
            return func
        return decorator

    def get(self, path):
        return self.route(path, 'GET')

    def post(self, path):
        return self.route(path, 'POST')

    def put(self, path):
        return self.route(path, 'PUT')

    def delete(self, path):
        return self.route(path, 'DELETE')

    def options(self, path):
        return self.route(path, 'OPTIONS')

    def require_login(self, func):
        @wraps(func)
        def wrapper(handler, *args, **kwargs):
            token = handler.headers.get('Authorization')
            if token in self.tokens:
                return func(handler, *args, **kwargs)
            else:
                handler.send_response(401)
                handler.end_headers()
                return {"error": "Unauthorized"}
        return wrapper

    def rate_limit(self, limit, period):
        def decorator(func):
            @wraps(func)
            def wrapper(handler, *args, **kwargs):
                ip = handler.client_address[0]
                now = time.time()
                if ip not in self.rate_limits:
                    self.rate_limits[ip] = []
                self.rate_limits[ip] = [timestamp for timestamp in self.rate_limits[ip] if now - timestamp < period]
                if len(self.rate_limits[ip]) < limit:
                    self.rate_limits[ip].append(now)
                    return func(handler, *args, **kwargs)
                else:
                    handler.send_response(429)
                    handler.end_headers()
                    return {"error": "Too Many Requests"}
            return wrapper
        return decorator

    def list_endpoints(self, handler):
        endpoints = [{"path": path, "methods": list(methods.keys())} for path, methods in self.routes.items()]
        handler.send_response(200)
        handler.send_header('Content-type', 'application/json')
        handler.end_headers()
        handler.wfile.write(json.dumps(endpoints).encode())

    def handle_request(self, handler, method):
        if handler.path == '/endpoints' and method == 'GET':
            self.list_endpoints(handler)
            return

        path = handler.path
        if path in self.routes and method in self.routes[path]:
            handler_func = self.routes[path][method]
            response = handler_func(handler)
            response_json = json.dumps(response).encode()
            handler.send_response(200)
            handler.send_header('Content-type', 'application/json')
            handler.send_header('Content-Length', str(len(response_json)))
            handler.end_headers()
            handler.wfile.write(response_json)
        else:
            handler.send_response(404)
            handler.end_headers()

    def start(self, host='localhost', port=8000):
        class RequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.server.framework.handle_request(self, 'GET')

            def do_POST(self):
                self.server.framework.handle_request(self, 'POST')

            def do_PUT(self):
                self.server.framework.handle_request(self, 'PUT')

            def do_DELETE(self):
                self.server.framework.handle_request(self, 'DELETE')

            def do_OPTIONS(self):
                self.server.framework.handle_request(self, 'OPTIONS')

        server = HTTPServer((host, port), RequestHandler)
        server.framework = self
        print(f"Starting server at http://{host}:{port}")
        server.serve_forever()

    def run_with_reload(self, host='localhost', port=8000):
        class RequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.server.framework.handle_request(self, 'GET')

            def do_POST(self):
                self.server.framework.handle_request(self, 'POST')

            def do_PUT(self):
                self.server.framework.handle_request(self, 'PUT')

            def do_DELETE(self):
                self.server.framework.handle_request(self, 'DELETE')

            def do_OPTIONS(self):
                self.server.framework.handle_request(self, 'OPTIONS')

        async def watch_file(file_path, callback):
            last_modified_time = os.path.getmtime(file_path)
            while True:
                current_modified_time = os.path.getmtime(file_path)
                if current_modified_time != last_modified_time:
                    last_modified_time = current_modified_time
                    callback()
                await asyncio.sleep(1)

        async def restart_server():
            while True:
                await asyncio.create_task(watch_file(__file__, lambda: os.execv(sys.executable, ['python'] + sys.argv)))

        async def start_server():
            server = HTTPServer((host, port), RequestHandler)
            server.framework = self
            print(f"Starting server at http://{host}:{port}")
            await asyncio.get_event_loop().run_in_executor(None, server.serve_forever)

        loop = asyncio.get_event_loop()
        loop.create_task(restart_server())
        loop.run_until_complete(start_server())
