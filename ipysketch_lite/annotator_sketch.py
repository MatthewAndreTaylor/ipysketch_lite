import base64
import io

from PIL import Image

from .sketch import Sketch


class AnnotationSketch(Sketch):
    """
    AnnotationSketch class to create an annotation sketch instance
    This includes a template that allows for basic annotation of an image
    """

    def __init__(self, image: Image):
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
        self.data_url = f"data:image/png;base64,{image_data}"

        super().__init__(image.width, image.height)

    def get_template(self) -> str:
        return (
            super().get_template()
            + f"""<script>var image = new Image();image.src = "{self.data_url}";ctx.drawImage(image, 0, 0);</script>"""
        )
