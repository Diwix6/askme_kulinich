# test.wsgi
def app(environ, start_response):
    from urllib.parse import parse_qs

    method = environ["REQUEST_METHOD"]
    if method == "GET":
        params = parse_qs(environ.get("QUERY_STRING", ""))
    elif method == "POST":
        try:
            request_body = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0)))
            params = parse_qs(request_body.decode())
        except Exception:
            params = {}

    start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8")])
    response_lines = [f"{k}: {v}" for k, v in params.items()]
    return ["\n".join(response_lines or ["No params received"]).encode("utf-8")]
