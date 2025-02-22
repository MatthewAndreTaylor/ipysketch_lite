#!/bin/bash

if [[ "$1" == "--clean" ]]; then
    echo "Cleaning build and html directories..."
    rm -rf ./docs/build
fi

pip install IPython sphinx sphinx-book-theme

sphinx-apidoc --no-toc -o ./docs ipysketch_lite
sphinx-build -M html ./docs ./docs/build -W