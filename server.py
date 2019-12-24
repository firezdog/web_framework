from webob import Request, Response

class Server:
    def __call__(self, environ, start_response):
        request = Request(environ)    # unused for now
        
        response = self.handle_request(request)
        
        return response(environ, start_response)
    
    def handle_request(self, request):
        user_agent = request.environ.get('HTTP_USER_AGENT', 'No user agent found')

        response = Response()
        response.text = f'User agent: {user_agent}'

        return response