# ipysketch_lite

A lite sketching utility for python notebooks, no sockets or extra dependencies 🎨

(no extra widget code)

Make sketches right in your notebook then use the sketch in your python code.

Try yourself:

<a href="https://matthewandretaylor.github.io/ipysketch_lite/jupyterlite/lab/index.html">
<img alt="jupyterlite badge" src="https://jupyterlite.rtfd.io/en/latest/_static/badge.svg">
</a>

## Quickstart

Start drawing a quick sketch in your notebook like this

```py
from ipysketch_lite import Sketch

sketch = Sketch()
```

Then add a new cell to retrieve the sketch in python

```py
print(sketch.get_output())

import matplotlib.pyplot as plt

plt.imshow(sketch.get_output_array())
```

![example sketch](https://github.com/MatthewAndreTaylor/ipysketch_lite/blob/main/sketches/example.png?raw=true)

Sketches get updated in cells after draw updates

This means you can continue your sketch and get the new updated outputs
