from ipysketch_lite import template

from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import logging
import base64
import io

from IPython.display import HTML, display
from IPython.utils import path


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        message = post_data.decode("utf-8")

        with open("message.txt", "w") as buffer:
            buffer.write(message)

        self.send_response(200)


def run(handler_class=SimpleHTTPRequestHandler, port=5000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, handler_class)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.start()


class Sketch:
    """
    Sketch class to create a sketch instance
    This includes a template that allows for basic drawing utilities
    """

    _data: str
    _logger: logging.Logger

    def __init__(self, width: int = 400, height: int = 300):
        self._data = ""
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.ERROR)

        self._send_first()
        self.metadata = {
            "{width}": width,
            "{height}": height,
            "{canvas_upload}": "window.sendMessage(canvas.toDataURL());",
        }

        try:
            run()
            self.metadata[
                "{canvas_upload}"
            ] = """fetch('http://localhost:5000', {method: 'POST', headers: {'Content-Type': 'text/plain'}, body: canvas.toDataURL()});"""
        except Exception as e:
            self._logger.warning(f"Could not start local server: {e} Using default method.")

        sketch_template = self.get_template()

        display(HTML(sketch_template))

    def get_template(self):
        sketch_template = template.template
        for key, value in self.metadata.items():
            sketch_template = sketch_template.replace(key, str(value))

        return sketch_template

    def _send_first(self):
        # Create a sample 1x1 px png image
        sample_data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAAtJREFUGFdjYAACAAAFAAGq1chRAAAAAElFTkSuQmCC"
        with open("message.txt", "w") as buffer:
            buffer.write(sample_data)

        # Touch the file to create it
        self._read_message_data()

    def _read_message_data(self) -> None:
        try:
            message_path = path.filefind("message.txt")
            if message_path:
                with open(message_path, "r") as f:
                    self._data = f.read()
        except Exception as e:
            raise e

    def save(self, path: str):
        """
        Save the sketch image data to a file
        """
        if not path.endswith(".png"):
            raise ValueError("Only PNG files are supported.")

        self.image.save(path)

    @property
    def data(self) -> str:
        """
        Get the sketch image data as a base64 encoded string
        """
        try:
            self._read_message_data()
        except Exception as e:
            self._logger.error(f"Could not read message data: {e}")
        return self._data

    @property
    def array(self):
        """
        Get the sketch image data as a numpy array
        """
        return self.get_output_array()

    @property
    def image(self):
        """
        Get the sketch image data as a PIL image
        """
        return self.get_output_image()

    def get_output(self) -> str:
        return self.data

    def get_output_image(self):
        try:
            from PIL import Image
        except ImportError:
            raise ImportError("PIL (Pillow) is required to use this method.")

        image_data = self.get_output().split(",")[1]
        bytesio = io.BytesIO(base64.b64decode(image_data))
        return Image.open(bytesio)

    def get_output_array(self):
        try:
            import numpy as np
        except ImportError:
            raise ImportError("Numpy is required to use this method.")

        image = self.get_output_image()
        return np.array(image)
