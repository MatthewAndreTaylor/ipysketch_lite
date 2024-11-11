from ipysketch_lite import Sketch, template


class SketchPad(Sketch):
    """
    SketchPad class to create a sketchpad instance
    This includes a template that allows for using different tools to draw on the sketchpad
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_template(self):
        sketch_template = template.pad_template
        for key, value in self.metadata.items():
            sketch_template = sketch_template.replace(key, str(value))

        return sketch_template
