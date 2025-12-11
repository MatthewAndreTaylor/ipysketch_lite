import base64
import io
import pathlib

from PIL import Image
from IPython.display import display

import anywidget
import traitlets

template_js_path = pathlib.Path(__file__).parent / "sketch.js"
template_css_path = pathlib.Path(__file__).parent / "sketch.css"


def _replace_all(s: str, d: dict) -> str:
    for key, value in d.items():
        s = s.replace(key, str(value))
    return s


class Sketch(anywidget.AnyWidget):
    """
    Sketch class to create a sketch instance
    This includes a template that allows for basic drawing utilities
    Sketch image data is stored as a base64 encoded string
    """

    _script_metadata: dict
    _sketch_data = traitlets.Unicode().tag(sync=True)
    _canvas_upload: str = (
        "model.set('_sketch_data', canvas.toDataURL());model.save_changes();"
    )

    def __init__(self, width: int = 400, height: int = 300):
        self._script_metadata = {
            "model.width": width,
            "model.height": height,
            "model.canvas_upload": self._canvas_upload,
        }

        self._esm = _replace_all(self.get_template(), self._script_metadata)
        self._css = template_css_path.read_text()
        super().__init__()
        display(self)

    def get_template(self) -> str:
        """
        Get the template JavaScript for the sketch widget
        """
        return template_js_path.read_text()

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
        return str(self._sketch_data)

    @property
    def image(self):
        """
        Get the sketch image data as a PIL image
        """
        try:
            image_data = self._sketch_data.split(",")[1]
            bytesio = io.BytesIO(base64.b64decode(image_data))
        except IndexError:
            raise ValueError("Not enough data to create an image")
        return Image.open(bytesio)


class AnnotationSketch(Sketch):
    """
    AnnotationSketch class to create a sketch instance with a base image
    This includes a template that allows for basic drawing utilities
    The base image is drawn on the canvas and can be annotated
    """

    def __init__(self, image: Image):
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
        self.data_url = f"data:image/png;base64,{image_data}"
        self._canvas_upload += (
            "}{"
            + f"""var base_im = new Image();base_im.src = "{self.data_url}";base_im.onload = function(){{ctx.drawImage(base_im, 0, 0);}}"""
        )
        super().__init__(image.width, image.height)
