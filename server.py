def server(environ, start_response):
    response_body = b'Hello world!'
    status = '200 OK'
    start_response(status, headers=[])
    return iter([response_body])