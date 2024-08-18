# Development docs

```bash

# Create env
conda create -n jupyterlab-ext --override-channels --strict-channel-priority -c conda-forge -c nodefaults jupyterlab=4 nodejs=20 git copier=9 jinja2-time

# Activate env
conda activate jupyterlab-ext

# Install dev (creates yarn.lock)
pip install -ve .

# Build package
jlpm run build


# Create sample lab test env
jupyter lab --notebook-dir=.

# Create sample lite test env
jupyter lite build

```
