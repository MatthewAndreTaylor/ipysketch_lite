from ipysketch_lite import Sketch, template


class SketchPad(Sketch):
    """
    SketchPad class to create a sketchpad instance
    This includes a template that allows for using different tools to draw on the sketchpad
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_template(self):
        return template.pad_template
