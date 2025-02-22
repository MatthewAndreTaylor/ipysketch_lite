import base64
import io
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from IPython.display import HTML, display
from PIL import Image

from .. import _template as template


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        message = post_data.decode("utf-8")
        self.sketch._data = message
        self.send_response(200)


def _run(handler_class=SimpleHTTPRequestHandler, port=5000, sketch=None):
    server_address = ("", port)
    handler_class.sketch = sketch
    httpd = HTTPServer(server_address, handler_class)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.start()


class LegacySketch:
    """
    Legacy Sketch class to create a sketch instance
    This includes a template that allows for basic drawing utilities
    small client for transferring image data
    """

    _data: str
    _logger: logging.Logger
    metadata: dict

    def __init__(self, width: int = 400, height: int = 300):
        self._data = ""
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.ERROR)
        
        self.metadata = {
            "{width}": width,
            "{height}": height,
            "{canvas_upload}": f"return;",
        }

        try:
            _run(sketch=self)
            self.metadata["{canvas_upload}"] = (
                f"""fetch('http://localhost:5000', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'text/plain'}},
                    body: canvas.toDataURL()
                }});"""
            )
        except Exception as e:
            self._logger.warning(f"Could not start local server: {e}")

        sketch_template = self.get_template()
        display(HTML(sketch_template))

    def get_template(self) -> str:
        """
        Get the sketch html template with metadata replaced
        """
        sketch_template = template.template_html
        for key, value in self.metadata.items():
            sketch_template = sketch_template.replace(key, str(value))

        return sketch_template

    def save(self, fp, file_format=None) -> None:
        """
        Save the sketch image data to a file
        """
        self.image.save(fp, format=file_format)

    @property
    def data(self) -> str:
        """
        Get the sketch image data as a base64 encoded string
        """
        return self._data

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
            image_data = self.get_output().split(",")[1]
            bytesio = io.BytesIO(base64.b64decode(image_data))
        except IndexError:
            raise ValueError("Not enough data to create an image")
        return Image.open(bytesio)
