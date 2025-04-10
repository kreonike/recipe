import json
import re


class WSGIApp:
    def __init__(self):
        self.routes = {}

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        method = environ['REQUEST_METHOD']

        for route_pattern, (handler, param_names) in self.routes.items():
            match = re.fullmatch(route_pattern, path)
            if match:
                kwargs = {
                    name: match.group(i + 1) for i, name in enumerate(param_names)
                }
                return handler(environ, start_response, **kwargs)

        return self.handle_404(start_response)

    def route(self, path):
        def decorator(handler):
            pattern, param_names = self._parse_route(path)
            self.routes[pattern] = (handler, param_names)
            return handler

        return decorator

    def _parse_route(self, path):
        param_names = []
        pattern_parts = []

        for part in path.split('/'):
            if part.startswith('<') and part.endswith('>'):
                param_name = part[1:-1].split(':')[0]
                param_names.append(param_name)
                pattern_parts.append('([^/]+)')
            else:
                pattern_parts.append(re.escape(part))

        pattern = '/'.join(pattern_parts)
        pattern = f'^{pattern}$'
        return pattern, param_names

    def handle_404(self, start_response):
        headers = [('Content-Type', 'application/json')]
        start_response('404 Not Found', headers)
        response = json.dumps({"error": "404 Not Found"}, indent=4)
        return [response.encode('utf-8')]


app = WSGIApp()


@app.route("/hello")
def say_hello(environ, start_response):
    headers = [('Content-Type', 'application/json')]
    start_response('200 OK', headers)
    response = json.dumps({"response": "Hello, world!"}, indent=4)
    return [response.encode('utf-8')]


@app.route("/hello/<name>")
def say_hello_with_name(environ, start_response, name):
    headers = [('Content-Type', 'application/json')]
    start_response('200 OK', headers)
    response = json.dumps({"response": f"Hello, {name}!"}, indent=4)
    return [response.encode('utf-8')]
