from webob import Request, Response

class Server:
    def __init__(self):
        self.routes = {}
    
    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        
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
