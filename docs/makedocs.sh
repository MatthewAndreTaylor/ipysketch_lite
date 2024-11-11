#!/bin/bash

pip install IPython sphinx sphinx-rtd-theme==2.0.0 m2r2==0.3.3

sphinx-build -M html ./docs ./docs/build -W