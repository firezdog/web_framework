from webob import Request, Response

class Server:
    def __call__(self, environ, start_response):
        # request = Request(environ)    # unused for now
        response = Response()
        with open('index.html') as html:
            response.text = html.read()
            return response(environ, start_response)