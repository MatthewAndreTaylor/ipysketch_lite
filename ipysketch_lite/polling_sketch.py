from ipysketch_lite import Sketch

import asyncio
import threading
from typing import Union


class PollingSketch(Sketch):
    """
    A PollingSketch polls the message data from the sketch and dynamically updates the data in the background
    """

    _is_polling: bool
    _thread: Union[threading.Thread, None]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._is_polling = False
        self._thread = None

    def start_polling(self):
        """
        Start polling the sketch data
        """
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

    def stop_polling(self):
        """
        Stop polling the sketch data
        """
        try:
            self._is_polling = False
            if self._thread:
                self._thread.join()
        except Exception as e:
            print(e)

    async def _poll_message_contents(self) -> None:
        while True:
            try:
                self.sketch._read_message_data()
            except:
                self._is_polling = False
            await asyncio.sleep(1)  # sleep for 1 second before next poll

    def _run_async(self) -> None:
        asyncio.run(self._poll_message_contents())

    @property
    def data(self) -> str:
        """
        Get the sketch image data as a base64 encoded string dynamically by polling the sketch
        """
        if self._is_polling:
            return self._data

        try:
            self._read_message_data()
        except Exception as e:
            print(e)
        return self._data
