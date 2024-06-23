import json
import logging

from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler

logging.basicConfig(level=logging.INFO)




class CemirFW:
    """
    CemirFW is a lightweight framework for building REST APIs using Tornado.
    """

    def __init__(self, host='localhost', port=8000, debug=False):
        """
        Initialize the CemirFW instance.

        Args:
            host (str, optional): Host IP address or hostname. Defaults to 'localhost'.
            port (int, optional): Port number. Defaults to 8000.
            debug (bool, optional): Enable debug mode. Defaults to False.
        """
        self.host = host
        self.port = port
        self.debug = debug
        self.routes = []

    def route(self, method, path):
        """
        Decorator function to register routes with specific HTTP methods.

        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE).
            path (str): URL path for the route.

        Returns:
            function: Decorated handler function.
        """

        def decorator(handler):
            self.routes.append((path, method, handler))
            return handler

        return decorator

    def get(self, path):
        """
        Decorator for registering a GET route.

        Args:
            path (str): URL path for the GET route.

        Returns:
            function: Decorated handler function.
        """
        return self.route('GET', path)

    def post(self, path):
        """
        Decorator for registering a POST route.

        Args:
            path (str): URL path for the POST route.

        Returns:
            function: Decorated handler function.
        """
        return self.route('POST', path)

    def put(self, path):
        """
        Decorator for registering a PUT route.

        Args:
            path (str): URL path for the PUT route.

        Returns:
            function: Decorated handler function.
        """
        return self.route('PUT', path)

    def delete(self, path):
        """
        Decorator for registering a DELETE route.

        Args:
            path (str): URL path for the DELETE route.

        Returns:
            function: Decorated handler function.
        """
        return self.route('DELETE', path)

    def run(self):
        """
        Start the Tornado server and run the application.
        """

        class TornadoRequestHandler(RequestHandler):
            """
            Request handler class for processing HTTP requests.
            """

            async def prepare(self):
                """
                Prepare method to parse request data before handling the request.
                """
                self.path = self.request.path
                self.method = self.request.method
                self.body = None
                if self.request.body:
                    try:
                        self.body = json.loads(self.request.body)
                    except json.JSONDecodeError:
                        self.body = self.request.body.decode()
                self.query_params = {k: v[0].decode() for k, v in self.request.query_arguments.items()}
                self.set_header('Server', 'CemirFW')

            async def get(self):
                """
                Handle GET requests.
                """
                await self.handle_method('GET')

            async def post(self):
                """
                Handle POST requests.
                """
                await self.handle_method('POST')

            async def put(self):
                """
                Handle PUT requests.
                """
                await self.handle_method('PUT')

            async def delete(self):
                """
                Handle DELETE requests.
                """
                await self.handle_method('DELETE')

            async def handle_method(self, method):
                """
                Method to handle the HTTP request based on the registered routes.

                Args:
                    method (str): HTTP method of the request.
                """
                for route_path, route_method, handler in fw.routes:
                    if route_method == method and self.match_path(route_path):
                        path_params = self.extract_path_params(route_path)
                        response = await handler(self, **path_params, **self.query_params)
                        if isinstance(response, tuple):
                            response_body, status_code = response
                        else:
                            response_body, status_code = response, 200

                        self.set_status(status_code)
                        self.set_header('Content-Type', 'application/json')
                        self.write(json.dumps(response_body))
                        return
                self.set_status(404)
                self.set_header('Content-Type', 'application/json')
                self.write(json.dumps({"error": "Route not found"}))

            def match_path(self, route_path):
                """
                Method to match the request path with registered route paths.

                Args:
                    route_path (str): Path of the registered route.

                Returns:
                    bool: True if there's a match, False otherwise.
                """
                route_parts = route_path.split('/')
                request_parts = self.path.split('/')
                if len(route_parts) != len(request_parts):
                    return False
                for route_part, request_part in zip(route_parts, request_parts):
                    if route_part != request_part and not route_part.startswith('{'):
                        return False
                return True

            def extract_path_params(self, route_path):
                """
                Method to extract path parameters from the request path.

                Args:
                    route_path (str): Path of the registered route.

                Returns:
                    dict: Dictionary containing extracted path parameters.
                """
                path_params = {}
                route_parts = route_path.split('/')
                request_parts = self.path.split('/')
                for route_part, request_part in zip(route_parts, request_parts):
                    if route_part.startswith('{') and route_part.endswith('}'):
                        param_name = route_part[1:-1]
                        path_params[param_name] = request_part
                return path_params

        def log_request(self, status_code=None):
            """
            Custom logging function to log HTTP request details.

            Args:
                status_code (int, optional): HTTP status code of the response. Defaults to None.
            """
            request = self.request
            if status_code is None:
                status_code = self.get_status()
            if status_code == 200:
                logging.info(f"\033[97m[**CemirFW**]\033[0m [{request.remote_ip}] \033[92m[{status_code}]\033[0m \033[97m[{request.method}]\033[0m [{request.uri}] [{request.headers.get('User-Agent')}]")
            elif status_code == 404:
                logging.info(f"\033[97m[**CemirFW**]\033[0m [{request.remote_ip}] \033[91m[{status_code}]\033[0m \033[97m[{request.method}]\033[0m [{request.uri}] [{request.headers.get('User-Agent')}]")
            elif status_code // 100 == 3:
                logging.info(f"\033[97m[**CemirFW**]\033[0m [{request.remote_ip}] \033[93m[{status_code}]\033[0m \033[97m[{request.method}]\033[0m [{request.uri}] [{request.headers.get('User-Agent')}]")
            elif status_code == 304:
                logging.info(f"\033[97m[**CemirFW**]\033[0m [{request.remote_ip}] \033[94m[{status_code}]\033[0m \033[97m[{request.method}]\033[0m [{request.uri}] [{request.headers.get('User-Agent')}]")
            elif status_code // 100 == 5:
                logging.info(f"\033[97m[**CemirFW**]\033[0m [{request.remote_ip}] \033[33m[{status_code}]\033[0m \033[97m[{request.method}]\033[0m [{request.uri}] [{request.headers.get('User-Agent')}]")
            else:
                logging.info(f"\033[97m[**CemirFW**]\033[0m [{request.remote_ip}] [{status_code}] \033[97m[{request.method}]\033[0m [{request.uri}] [{request.headers.get('User-Agent')}]")

        app = Application([
            (r".*", TornadoRequestHandler)
        ], debug=self.debug, log_function=log_request)
        app.listen(self.port, address=self.host)
        logging.info(f"Starting server on {self.host}:{self.port}")
        IOLoop.current().start()


fw = CemirFW()
fw.run()
