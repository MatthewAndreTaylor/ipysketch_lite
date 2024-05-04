from http.server import BaseHTTPRequestHandler, HTTPServer
from IPython.display import HTML, display
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

        html_code = f"""<canvas id="canvas" width="{width}" height="{height}" style="border: 2px solid black;"></canvas>"""
        html_code += """
        <button onclick="clearCanvas()">clear</button>
        <input id="color" type="color" value="#000000"/>
        <script>
        var canvas = document.getElementById('canvas');
        var colorInput = document.getElementById('color');
        var ctx = canvas.getContext('2d');
        ctx.lineWidth = 4;
        ctx.lineJoin = "round";
        var drawing = false;
        var mouse = {x: 0, y: 0};
        
        fetch('http://localhost:5000', {
            method: 'POST',
            headers: {
            'Content-Type': 'text/plain',
            },
            body: canvas.toDataURL()
        })

        canvas.addEventListener('mousedown', (e) => {
            mouse = {x: e.offsetX, y: e.offsetY};
            drawing = true;
        });

        canvas.addEventListener('mousemove', (e) => {
            if (drawing) {
                drawLine(ctx, mouse.x, mouse.y, e.offsetX, e.offsetY);
                mouse = {x: e.offsetX, y: e.offsetY};
            }
        });

        canvas.addEventListener('mouseup', (e) => {
            if (drawing) {
                drawLine(ctx, mouse.x, mouse.y, e.offsetX, e.offsetY);
                drawing = false;
            }
            
            fetch('http://localhost:5000', {
                method: 'POST',
                headers: {
                'Content-Type': 'text/plain',
                },
                body: canvas.toDataURL()
            })
        });

        function drawLine(context, x1, y1, x2, y2) {
            ctx.strokeStyle = colorInput.value;
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.closePath();
            ctx.stroke();
        }

        function clearCanvas() {
            ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        }
        </script>
        """

        display(HTML(html_code))
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
