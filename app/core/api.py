import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class ApiRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, ref_req, api_ref):
        self.api = api_ref
        super().__init__(request, client_address, ref_req)

    def call_api(self, method, path, args):
        if path in self.api.routing[method]:
            try:
                result = self.api.routing[method][path](args)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(result, indent=4).encode())
            except Exception as e:
                self.send_response(500, "Server Error")
                self.end_headers()
                self.wfile.write(json.dumps({"error": e.args}, indent=4).encode())
        else:
            self.send_response(404, "Not Found")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "not found"}, indent=4).encode())

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        args: dict[str, list[str]] = parse_qs(parsed_url.query)

        for k in args.keys():
            if len(args[k]) == 1:
                args[k] = args[k][0]  # type: ignore

        self.call_api("GET", path, args)

    def do_POST(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        if self.headers.get("content-type") != "application/json":
            self.send_response(400)
            self.end_headers()
            self.wfile.write(
                json.dumps(
                    {"error": "posted data must be in json format"}, indent=4
                ).encode()
            )
        else:
            data_len = int(self.headers.get("content-length"))  # type: ignore
            data = self.rfile.read(data_len).decode()
            self.call_api("POST", path, json.loads(data))


class API:
    def __init__(self) -> None:
        self.routing = {"GET": {}, "POST": {}}

    def get(self, path):
        def wrapper(fn) -> None:
            self.routing["GET"][path] = fn

        return wrapper

    def post(self, path):
        def wrapper(fn) -> None:
            self.routing["POST"][path] = fn

        return wrapper

    def __call__(self, request, client_address, ref_request):
        api_handler = ApiRequestHandler(
            request, client_address, ref_request, api_ref=self
        )
        return api_handler
