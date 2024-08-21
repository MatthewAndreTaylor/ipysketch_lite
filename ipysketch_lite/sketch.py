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

    _data: str
    _is_polling: bool
    _thread: threading.Thread | None

    def __init__(self, width: int = 400, height: int = 300):
        self._is_polling = False
        self._thread = None

        self._data = ""
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
        self._read_message_data()

        display(HTML(sketch_template))

    def start_polling(self) -> None:
        self._is_polling = True
        try:
            # run this in a separate thread
            self._thread = threading.Thread(target=self._run_async)
            self._thread.start()
        except Exception as e:
            try:
                asyncio.ensure_future(self._poll_message_contents())
                asyncio.get_event_loop().run_forever()
            except Exception as e:
                self._is_polling = False
                print(e)

    def stop_polling(self) -> None:
        try:
            self._is_polling = False
            if self._thread:
                self._thread.join()
        except Exception as e:
            print(e)

    async def _poll_message_contents(self) -> None:
        while True:
            try:
                self._read_message_data()
            except:
                self._is_polling = False
            await asyncio.sleep(1)  # sleep for 1 second before next poll

    def _run_async(self) -> None:
        asyncio.run(self._poll_message_contents())

    def _read_message_data(self) -> None:
        try:
            message_path = path.filefind("message.txt")
            if message_path:
                with open(message_path, "r") as f:
                    self._data = f.read()
        except Exception as e:
            raise e

    def save(self, path: str) -> None:
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
        if self._is_polling:
            return self._data

        try:
            self._read_message_data()
        except Exception as e:
            print(e)
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
