from webob import Request, Response
from parse import parse


class Server:
    def __init__(self):
        self.routes = {}

    ''' in an application, we write methods and decorate them with a call to route, 
        
        [1] @app.route('path') 
    
    vs. just

        [2] @app.route

    as in the examples I find for decorators on some reference sites.  I'm not 100% clear on what's happening, but it seems like when you just write the decorator out as in [2] the function below is replaced with the return of the decorating function -- whereas the effect of [1] is also to call that function (what we desire, because then the function defined is set as the handler for that path in our route dictionary).
    '''

    def route(self, path):
        dog = parse(path, '/hello/jerry')
        try:
            print(dog.named)
        except:
            pass
        def wrapper(handler):
            self.routes[path] = handler

        return wrapper

    def __call__(self, environment, start_response):
        request = Request(environment)
        response = self.handle_request(request)
        return response(environment, start_response)

    def handle_request(self, request):
        response = Response()
        handler = self.routes.get(request.path, None)
        # as written, routes have side effects but the response itself must still be returned.
        if handler is not None:
            handler(request, response)
        else:
            self.default_handler(request, response)
        return response

    def default_handler(self, request, response):
        response.text = "Route not found."
        # TODO -- test should assert that this is 404?  Problem is that as far as API is concerned, response is a private variable.
        response.status_code = 404
