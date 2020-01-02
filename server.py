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
        handler = self.get_route(request.path)
        # as written, routes have side effects but the response itself must still be returned.
        if handler is not None:
            handler(request, response)
        else:
            default_handler(request, response)
        return response

    def get_route(self, path):
        print(path)
        if path == "/":
            return self.root.handler
        else:
            path_list = path.strip('/').split('/')
            print(path_list)
            head = self.root
            for branch in path_list:
                branch_found = False
                for child in head.children:
                    if child.path == branch:
                        print(f'found {child.path}')
                        branch_found = True
                        head = child
                        break
                if not branch_found:
                    return default_handler
            return head.handler

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
            head.handler = handler
