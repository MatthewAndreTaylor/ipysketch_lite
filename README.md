# ipysketch_lite

A lite sketching utility for python notebooks, no sockets or extra dependencies 🎨

(no extra widget code)

Make sketches right in your notebook then use the sketch in your python code.

Try yourself:

<a href="https://matthewandretaylor.github.io/ipysketch_lite/jupyterlite/lab/index.html">
<img alt="jupyterlite badge" src="https://jupyterlite.rtfd.io/en/latest/_static/badge.svg">
</a>

[![PyPI](https://img.shields.io/pypi/v/ipysketch-lite.svg)](https://pypi.org/project/ipysketch-lite)
[![Docs](https://img.shields.io/badge/Docs-informational?logo=readthedocs&logoColor=white)](https://matthewandretaylor.github.io/ipysketch_lite/docs)

## Quickstart

To get started pip install the extension from [PyPI](https://pypi.org/project/ipysketch-lite)

This can be done using `pip` for jupyter environments

```bash
pip install ipysketch-lite
```

Or using `piplite` if you are using [jupyter lite](https://matthewandretaylor.github.io/ipysketch_lite/jupyterlite/lab/index.html)

```py
import piplite
await piplite.install("ipysketch_lite[extra]") # install the package and optionally pillow and numpy for the extra features
```

Start drawing a quick sketch in your notebook like this

```py
from ipysketch_lite import Sketch

sketch = Sketch()
```

Then add a new cell to retrieve the sketch in python

```py
sketch.data # Sketch image data as a base64 encoded string
```

```py
import matplotlib.pyplot as plt

# Plot the sketch image or do image manipulation
plt.imshow(sketch.image)
plt.show()
```

![example sketch](https://github.com/MatthewAndreTaylor/ipysketch_lite/blob/main/sketches/example.png?raw=true)

Sketches get updated in cells after draw updates

This means you can continue your sketch and get the new updated outputs
