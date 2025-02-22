import base64
import io
import logging

from PIL import Image

import anywidget
import traitlets

from ._template import template_js, template_css


class Sketch(anywidget.AnyWidget):
    """
    Sketch class to create a sketch instance
    This includes a template that allows for basic drawing utilities
    Sketch image data is stored as a base64 encoded string
    """

    _logger: logging.Logger
    metadata: dict
    _sketch_data = traitlets.Unicode().tag(sync=True)

    _canvas_upload: str = "model.set('_sketch_data', canvas.toDataURL());model.save_changes();"
    
    def __init__(self, width: int = 400, height: int = 300):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.ERROR)
        
        self.metadata = {
            "{width}": width,
            "{height}": height,
            "{canvas_upload}": self._canvas_upload,
        }

        sketch_template = self.get_template()
        self._esm = sketch_template
        self._css = template_css
        super().__init__()
        display(self)

    def get_template(self) -> str:
        """
        Get the sketch html template with metadata replaced
        """
        sketch_template = template_js
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
        return str(self._sketch_data)

    
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


class AnnotationSketch(Sketch):
    def __init__(self, image: Image):
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
        self.data_url = f"data:image/png;base64,{image_data}"
        self._canvas_upload += "}{" + f"""var base_im = new Image();base_im.src = "{self.data_url}";base_im.onload = function(){{ctx.drawImage(base_im, 0, 0);}}"""
        super().__init__(image.width, image.height)