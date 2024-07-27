# ipysketch_lite

A lite sketching utility for python notebooks, no sockets or extra dependencies 🎨

(no extra widget code)

Make sketches right in your notebook then use the sketch in your python code.

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

![example sketch](examples/sketches/example.png)

Sketches get updated in cells after draw updates

This means you can continue your sketch and get the new updated outputs
