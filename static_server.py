from urllib.parse import parse_qs

def app(environ, start_response):
    method = environ['REQUEST_METHOD']
    if method == 'GET':
        params = parse_qs(environ['QUERY_STRING'])
    elif method == 'POST':
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = environ['wsgi.input'].read(request_body_size)
        params = parse_qs(request_body.decode())
    else:
        params = {}

    response = '\n'.join(f'{k}: {v}' for k, v in params.items())
    response = response.encode('utf-8')

    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [response]
