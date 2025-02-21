from .annotator_sketch import AnnotationSketch
from .sketch import Sketch


def _jupyter_labextension_paths():
    return [{"src": "labextension", "dest": "ipysketch_lite"}]
