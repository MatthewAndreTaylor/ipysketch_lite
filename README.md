# ipysketch_lite 🎨

[![PyPI](https://img.shields.io/pypi/v/ipysketch-lite.svg)](https://pypi.org/project/ipysketch-lite)
[![Docs](https://img.shields.io/badge/Docs-informational?logo=readthedocs&logoColor=white)](https://matthewandretaylor.github.io/ipysketch_lite)
[![Jupyterlite](https://jupyterlite.rtfd.io/en/latest/_static/badge.svg)](https://matthewandretaylor.github.io/ipysketch_lite/jupyterlite/lab?path=lite_example.ipynb)


**ipysketch_lite** is a simple interactive sketching tool for Jupyter notebooks.
After drawing a sketch you can use it directly in your Jupyter notebook.
When changes are made to the sketch, the image data in Python is updated.


![demo](https://github.com/user-attachments/assets/32504e77-a9d1-43c2-96ff-dc0acff48393)

Try it out in JupyterLite: [![Jupyterlite](https://jupyterlite.rtfd.io/en/latest/_static/badge.svg)](https://matthewandretaylor.github.io/ipysketch_lite/jupyterlite/lab?path=lite_example.ipynb)


## Documentation 📖

You can view the documentation at: https://matthewandretaylor.github.io/ipysketch_lite


## Install 🛠️

You can install using **pip**:

```bash
pip install ipysketch-lite
```

Or using **piplite** if you are using [Jupyter lite](https://matthewandretaylor.github.io/ipysketch_lite/jupyterlite/lab?path=lite_example.ipynb)

```py
import piplite
await piplite.install("ipysketch_lite")
```

## Quickstart 🚀

Start drawing a quick sketch in your notebook like this

```py
from ipysketch_lite import Sketch

sketch = Sketch()
```

Then add a new cell to retrieve the sketch data in python

```py
sketch.data # Sketch image data as a base64 encoded string
sketch.image # PIL Image of the sketch
```

![example sketch](https://github.com/MatthewAndreTaylor/ipysketch_lite/blob/main/docs/_static/example.png?raw=true)

Sketch data gets updated in cells after the sketch is modified.
This means you can edit your sketch and get the new updated outputs


## Using your own drawing API 🖌️

You can extend `ipysketch_lite` to use your own JavaScript drawing library by customizing the frontend template. For example, you can integrate libraries by subclassing `Sketch` and providing a custom template.

See the [custom_sketch.ipynb](examples/custom_sketch.ipynb) notebook for a full example.

Here's a minimal example:

```python
from ipysketch_lite import Sketch

custom_template = """
function render({ model, el }) {
	// Load your drawing library and initialize the editor
}
export default { render };
"""

class CustomSketch(Sketch):
		def get_template(self):
				return custom_template

sketch = CustomSketch()
```

You can update the template to use any drawing API and connect it to Python as needed. The sketch data will update in your notebook after edits.

---