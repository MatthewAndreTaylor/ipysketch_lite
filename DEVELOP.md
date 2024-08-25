# Development docs

## Development environment

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

## Development deployment

There are two packages which are deployed.

a pure python package for `jupyterlite` environments which uses setuptools build.

an extension package for standard `jupyter` environments which uses hatch build.
