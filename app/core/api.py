import json
from http.server import BaseHTTPRequestHandler
from typing import Any, Callable
from urllib.parse import urlparse, parse_qs


class ApiRequestHandler(BaseHTTPRequestHandler):
    def __init__(
        self, request: Any, client_address: Any, ref_req: Any, api_ref: "API"
    ) -> None:
        self.api = api_ref
        super().__init__(request, client_address, ref_req)

    def call_api(self, method: str, path: str, args: Any) -> None:
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

    def do_GET(self) -> None:
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        args: dict[str, list[str]] = parse_qs(parsed_url.query)

        for k in args.keys():
            if len(args[k]) == 1:
                args[k] = args[k][0]  # type: ignore

        self.call_api("GET", path, args)

    def do_POST(self) -> None:
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
        self.routing: dict[str, dict[str, Callable[[Any], Any]]] = {
            "GET": {},
            "POST": {},
        }

    def get(self, path: str) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        def wrapper(fn: Callable[[Any], Any]) -> Callable[[Any], Any]:
            self.routing["GET"][path] = fn
            return fn

        return wrapper

    def post(self, path: str) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        def wrapper(fn: Callable[[Any], Any]) -> Callable[[Any], Any]:
            self.routing["POST"][path] = fn
            return fn

        return wrapper

    def __call__(
        self, request: Any, client_address: Any, ref_request: Any
    ) -> ApiRequestHandler:
        api_handler = ApiRequestHandler(
            request, client_address, ref_request, api_ref=self
        )
        return api_handler
