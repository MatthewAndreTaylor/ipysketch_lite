from .sketch import Sketch
from .sketchpad import SketchPad
from .polling_sketch import PollingSketch


def _jupyter_labextension_paths():
    return [{"src": "labextension", "dest": "ipysketch_lite"}]
