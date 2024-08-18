import asyncio
import threading
import base64
import io

from IPython.display import HTML, display
from IPython.utils import path

from .template import template

try:
    import numpy as np
    from PIL import Image

    PIL_INSTALLED = True
except ImportError:
    PIL_INSTALLED = False


class Sketch:
    """
    Sketch class to create a sketch instance
    """

    data: str
    is_polling: bool
    thread: threading.Thread

    def __init__(self, width: int = 400, height: int = 300):
        self.is_polling = False
        self.data = ""
        metadata = {
            "{width}": width,
            "{height}": height,
        }

        sketch_template = template
        for key, value in metadata.items():
            sketch_template = sketch_template.replace(key, str(value))

        display(HTML(sketch_template))

    def start_polling(self):
        self.is_polling
        try:
            # run this in a separate thread
            self.thread = threading.Thread(target=self.run_async)
            self.thread.start()
        except Exception as e:
            try:
                asyncio.ensure_future(self.poll_message_contents())
                asyncio.get_event_loop().run_forever()
            except Exception as e:
                self.is_polling = False
                print(e)

    def finish(self):
        try:
            self.is_polling = False
            self.thread.join()
        except Exception as e:
            print(e)

    def run_async(self):
        asyncio.run(self.poll_message_contents())

    async def poll_message_contents(self):
        while True:
            try:
                message_path = path.filefind("message.txt")
                if message_path:
                    with open(message_path, "r") as f:
                        self.data = f.read()
            except Exception as e:
                self.is_polling = False
                pass
            await asyncio.sleep(1)  # sleep for 1 second before next poll

    def get_output(self) -> str:
        if self.is_polling:
            return self.data

        try:
            message_path = path.filefind("message.txt")
            if message_path:
                with open(message_path, "r") as f:
                    self.data = f.read()
        except Exception as e:
            print(e)
            pass

    def get_output_array(self):
        if PIL_INSTALLED:
            image_data = self.data.split(",")[1]
            image = Image.open(io.BytesIO(base64.b64decode(image_data)))
            return np.array(image)
        else:
            raise ImportError("PIL (Pillow) and NumPy are required to use this method.")
