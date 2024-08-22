#!/bin/bash

pip install IPython sphinx sphinx-rtd-theme m2r2

sphinx-build -M html ./docs ./docs/build --fail-on-warning