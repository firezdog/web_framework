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
        handler = self.routes.get(req.path, None)
        # as written, routes have side effects but the response itself must still be returned.
        if handler is not None:
            handler(req, res)
        else:
            self.default_handler(req, res)
        return res
    

    def default_handler(self, req, res):
        res.text = "Route not found."
        res.status_code = 404   # TODO -- test should assert that this is 404
