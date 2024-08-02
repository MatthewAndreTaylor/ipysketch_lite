from .sketch import Sketch
from .sketchpad import SketchPad


def _jupyter_labextension_paths():
    return [{"src": "labextension", "dest": "ipysketch_lite"}]
