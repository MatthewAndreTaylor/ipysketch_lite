.. meta::
   :author: Matthew Taylor
   :description: ipysketch_lite - A simple sketching tool for Jupyter notebooks.
   :keywords: Jupyter, sketch, drawing, notebook, ipysketch_lite

ipysketch_lite 🎨
==========================================

**ipysketch_lite** is a simple interactive sketching tool for Jupyter notebooks.
After drawing a sketch you can use it directly in your Jupyter notebook.
When changes are made to the sketch, the image data in Python is updated.


Start sketching now 🖌️
-----------------------
You can start sketching now without having to install anything on your computer.

.. raw:: html
   :file: _static/sketch.html


|

Try it out in JupyterLite: |badge|

.. |badge| image:: https://jupyterlite.rtfd.io/en/latest/_static/badge.svg
   :target: https://matthewandretaylor.github.io/ipysketch_lite/jupyterlite/lab?path=lite_example.ipynb
   :alt: Launch JupyterLite


Install 🛠️
--------------------

You can install using **pip**:

.. code-block:: bash

   pip install ipysketch-lite


Or using **piplite** if you are using JupyterLite:

.. code-block:: python

   import piplite
   await piplite.install("ipysketch_lite")


API Reference 📚
-----------------

.. toctree::
   :maxdepth: 4

   ipysketch_lite



Quickstart 🚀
-----------------

Start drawing a quick sketch in your notebook like this

.. code-block:: python

   from ipysketch_lite import Sketch
   
   sketch = Sketch()

Then add a new cell to retrieve the sketch data in python

.. code-block:: python

   sketch.data # Sketch image data as a base64 encoded string
   sketch.image # PIL Image of the sketch


.. image:: https://github.com/MatthewAndreTaylor/ipysketch_lite/blob/main/docs/_static/example.png?raw=true
      :alt: example sketch

Sketch data gets updated in cells after the sketch is modified.
This means you can edit your sketch and get the new updated outputs

Using your own drawing API 🖌️
-----------------------------

You can extend ``ipysketch_lite`` to use your own JavaScript drawing library by subclassing ``Sketch`` and customizing the frontend template.
See the `custom_sketch.ipynb <https://github.com/MatthewAndreTaylor/ipysketch_lite/blob/main/examples/custom_sketch.ipynb>`_ notebook for an example.

* :ref:`genindex`
* :ref:`search`