from webob import Request, Response
from parse import parse


class Route:
    def __init__(self, path, handler):
        self.children = []
        self.path = path
        self.handler = handler


def default_handler(request, response):
    response.text = "Route not found."
    response.status_code = 404


class RouteAlreadyExistsException(Exception):
    pass


class Server:
    def __init__(self):
        self.root = Route(path='/', handler=default_handler)

    def route(self, path):
        def wrapper(handler):
            self.add_route(path, handler)

        return wrapper

    def __call__(self, environment, start_response):
        request = Request(environment)
        response = self.handle_request(request)
        return response(environment, start_response)

    def handle_request(self, request):
        response = Response()
        handler, params = self.get_route(request.path)
        # as written, routes have side effects but the response itself must still be returned.
        if handler is not None:
            handler(request, response, **params)
        else:
            default_handler(request, response)
        return response

    def get_route(self, path):
        params = {}
        if path == "/":
            return self.root.handler, params
        else:
            path_list = path.strip('/').split('/')
            head = self.root
            for branch in path_list:
                branch_found = False
                for child in head.children:
                    parse_result = parse(child.path, branch)
                    if parse_result:
                        params.update(parse_result.named)
                        branch_found = True
                        head = child
                        break
                if not branch_found:
                    return default_handler, params
            return head.handler, params

    def add_route(self, path, handler):
        if path == "/":
            self.root = Route(path, handler)
        else:
            path_list = path.strip('/').split('/')
            head = self.root
            for branch in path_list:
                branch_found = False
                for child in head.children:
                    if child.path == branch:
                        branch_found = True
                        head = child
                        break
                if not branch_found:
                    new_branch = Route(path=branch, handler=default_handler)
                    head.children.append(new_branch)
                    head = new_branch
            if head.handler == default_handler or head.handler is None:
                head.handler = handler
            else:
                raise RouteAlreadyExistsException
