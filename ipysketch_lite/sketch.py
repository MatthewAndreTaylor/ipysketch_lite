from ipysketch_lite import template

import asyncio
import threading
import base64
import io

from IPython.display import HTML, display
from IPython.utils import path


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

        sketch_template = template.template
        for key, value in metadata.items():
            sketch_template = sketch_template.replace(key, str(value))

        # Create a sample 1x1 px png image
        sample_data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAAtJREFUGFdjYAACAAAFAAGq1chRAAAAAElFTkSuQmCC"
        with open("message.txt", "w") as buffer:
            buffer.write(sample_data)

        # Touch the file to create it
        self.read_message_data()

        display(HTML(sketch_template))

    def start_polling(self):
        self.is_polling = True
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

    async def poll_message_contents(self):
        while True:
            try:
                self.read_message_data()
            except:
                self.is_polling = False
            await asyncio.sleep(1)  # sleep for 1 second before next poll

    def run_async(self):
        asyncio.run(self.poll_message_contents())

    def read_message_data(self):
        try:
            message_path = path.filefind("message.txt")
            if message_path:
                with open(message_path, "r") as f:
                    self.data = f.read()
        except Exception as e:
            raise e

    def get_output(self) -> str:
        if self.is_polling:
            return self.data

        try:
            self.read_message_data()
        except Exception as e:
            print(e)
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
