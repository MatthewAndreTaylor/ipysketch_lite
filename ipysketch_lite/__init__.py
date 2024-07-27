from http.server import BaseHTTPRequestHandler, HTTPServer
from IPython.display import HTML, display
from .gen import template
import threading
import base64
import io

try:
    from PIL import Image
    import numpy as np

    PIL_INSTALLED = True
except ImportError:
    PIL_INSTALLED = False


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        message = post_data.decode("utf-8")

        global output
        output = message

        global response_received
        response_received.set()

        self.send_response(200)


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=5000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.start()


class Sketch:
    def __init__(self, width: int = 400, height: int = 300):
        global response_received
        response_received = threading.Event()
        run()

        metadata = {
            "{width}": width,
            "{height}": height,
        }

        sketch_template = template
        for key, value in metadata.items():
            sketch_template = sketch_template.replace(key, str(value))

        display(HTML(sketch_template))
        response_received.wait()

    def get_output(self) -> str:
        return output

    def get_output_array(self) -> np.ndarray:
        if PIL_INSTALLED:
            image_data = output.split(",")[1]
            image = Image.open(io.BytesIO(base64.b64decode(image_data)))
            return np.array(image)
        else:
            raise ImportError("PIL (Pillow) and NumPy are required to use this method.")
