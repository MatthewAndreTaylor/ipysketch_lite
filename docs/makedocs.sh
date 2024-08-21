#!/bin/bash

pip install sphinx-rtd-theme

sphinx-build -M html ./docs/ ./build --fail-on-warning