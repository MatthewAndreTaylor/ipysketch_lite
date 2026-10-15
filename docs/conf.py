import inspect
import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "ipysketch_lite"
copyright = "2025, Matthew Taylor"
author = "Matthew Taylor"

extensions = ["sphinx.ext.autodoc"]


def _use_class_signature(app, what, name, obj, options, signature, return_annotation):
    if what == "class" and name.startswith("ipysketch_lite."):
        return str(inspect.signature(obj)), return_annotation


def setup(app):
    app.connect("autodoc-process-signature", _use_class_signature)

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", ".pyc"]

html_theme = "sphinx_book_theme"
html_favicon = "_static/icon.ico"
html_logo = "_static/icon.ico"

html_static_path = [
    "_static",
    "../ipysketch_lite/vector_sketch.js",
    "../ipysketch_lite/sketch.css",
]
templates_path = ["_templates"]
html_css_files = ["custom.css"]

html_sidebars = {
    "**": [
        "navbar-logo.html",
        "icon-links.html",
        "search-button-field.html",
        "sbt-sidebar-nav.html",
        "custom-sidebar.html",
    ],
}

html_theme_options = {
    "path_to_docs": "docs",
    "repository_url": "https://github.com/MatthewAndreTaylor/ipysketch_lite",
    "repository_branch": "main",
    "use_source_button": True,
    "use_issues_button": True,
    "use_download_button": True,
    "use_sidenotes": True,
    "home_page_in_toc": True,
    "show_toc_level": 2,
    "logo": {
        "text": project,
    },
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/MatthewAndreTaylor/ipysketch_lite",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/ipysketch-lite",
            "icon": "https://img.shields.io/pypi/dw/ipysketch_lite",
            "type": "url",
        },
        {
            "name": "JupyterLite",
            "url": "https://matthewandretaylor.github.io/ipysketch_lite/jupyterlite/lab?path=quickstart.ipynb",
            "icon": "https://jupyterlite.rtfd.io/en/latest/_static/badge.svg",
            "type": "url",
        },
        {
            "name": "Open In Colab",
            "url": "https://colab.research.google.com/github/MatthewAndreTaylor/ipysketch_lite/blob/main/examples/quickstart.ipynb",
            "icon": "https://colab.research.google.com/assets/colab-badge.svg",
            "type": "url",
        },
    ],
}
