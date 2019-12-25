from webob import Request, Response

class Server:
    def __init__(self):
        self.routes = {}
    
    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        
        return wrapper


    def __call__(self, environ, start_response):
        request = Request(environ)        
        response = self.handle_request(request)
        res = response(environ, start_response)
        return res
    
    def handle_request(self, req):
        res = Response()
        route = self.routes.get(req.path, None)
        if route is not None:
            route(req, res)
        else:
            res.text = 'Route not found.'
        return res