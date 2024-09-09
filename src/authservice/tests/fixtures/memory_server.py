"""Alternative to the aioresponses lib"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from urllib.parse import urlparse

import json

from src.services.notification.config import VERIFICATION_TOKEN_URL


last_request_body = None


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)

        self.send_response(200)
        self.end_headers()

        global last_request_body
        last_request_body = json.loads(body.decode("utf-8"))


class MemoryServer(HTTPServer):
    def __init__(self, host, port, *args, **kwargs):
        super().__init__(
            *args,
            server_address=(host, port),
            RequestHandlerClass=RequestHandler,
            **kwargs,
        )

    def __enter__(self):
        self._thread = Thread(target=self.serve_forever)
        self._thread.start()
        return self

    def __exit__(self, *args):
        super().__exit__(*args)
        self.shutdown()
        self._thread.join()


# @pytest.fixture(scope="session", autouse=True)
def setup_memory_server():
    parsed_url = urlparse(VERIFICATION_TOKEN_URL)
    with MemoryServer(parsed_url.hostname, parsed_url.port):
        yield
