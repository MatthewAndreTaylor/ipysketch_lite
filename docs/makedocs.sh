#!/bin/bash

pip install sphinx-rtd-theme m2r2

sphinx-build -M html ./docs/ ./build --fail-on-warning