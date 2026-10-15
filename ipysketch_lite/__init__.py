import base64
import io
import pathlib
from abc import ABCMeta, abstractmethod

from PIL import Image
from IPython.display import display

import anywidget
import traitlets

template_js_path = pathlib.Path(__file__).parent / "sketch.js"
template_css_path = pathlib.Path(__file__).parent / "sketch.css"
template_vector_js_path = pathlib.Path(__file__).parent / "vector_sketch.js"


def _replace_all(s: str, d: dict) -> str:
    for key, value in d.items():
        s = s.replace(key, str(value))
    return s


class _SketchWidgetMeta(type(anywidget.AnyWidget), ABCMeta):
    """Combine traitlets widget initialization with abstract method enforcement."""


class BaseSketchWidget(anywidget.AnyWidget, metaclass=_SketchWidgetMeta):
    """
    Abstract base for widget setup, image synchronization, and saving.
    Subclasses provide their drawing frontend through get_template.
    """

    _script_metadata: dict
    _sketch_data = traitlets.Unicode().tag(sync=True)

    def __init__(self, width: int = 400, height: int = 300):
        self._script_metadata = {
            "model.width": width,
            "model.height": height,
        }

        self._esm = _replace_all(self.get_template(), self._script_metadata)
        self._css = template_css_path.read_text()
        super().__init__()
        display(self)

    @abstractmethod
    def get_template(self) -> str:
        """
        Return the subclass's JavaScript drawing template.
        """
        raise NotImplementedError("Sketch widgets must provide a JavaScript template")

    @property
    def data(self) -> str:
        """
        Get the sketch image data as a base64 encoded string
        """
        return str(self._sketch_data)

    @property
    def image(self) -> Image.Image:
        """
        Get the sketch image data as a PIL image
        """
        try:
            image_data = self._sketch_data.split(",")[1]
            bytesio = io.BytesIO(base64.b64decode(image_data))
        except IndexError:
            raise ValueError("Not enough data to create an image")
        return Image.open(bytesio)


class RasterSketch(BaseSketchWidget):
    """Canvas-based sketch widget storing raster image data."""

    def get_template(self) -> str:
        return template_js_path.read_text()


class AnnotationSketch(BaseSketchWidget):
    """
    AnnotationSketch class to create a sketch instance with a base image
    This includes a template that allows for basic drawing utilities
    The base image is drawn on the canvas and can be annotated
    """

    data_url = traitlets.Unicode().tag(sync=True)

    def __init__(self, base_image: Image.Image):
        buffer = io.BytesIO()
        base_image.save(buffer, format="PNG")
        image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
        self.data_url = f"data:image/png;base64,{image_data}"
        super().__init__(base_image.width, base_image.height)

    def get_template(self) -> str:
        return template_js_path.read_text()


class Sketch(BaseSketchWidget):
    """
    Default sketch widget with vector strokes, bucket fill, and adjustable line width.
    This includes a template that allows for basic vector drawing utilities
    Sketch image data is stored as a base64 encoded string, and SVG data is also available
    """

    _svg_data = traitlets.Unicode().tag(sync=True)

    @property
    def svg(self) -> str:
        """
        Get the sketch SVG data as a string
        """
        return str(self._svg_data)

    def get_template(self) -> str:
        """
        Get the template JavaScript for the vector sketch widget
        """
        return template_vector_js_path.read_text()
