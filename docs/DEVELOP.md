# Development docs

## Development environment

```bash
# Setup env
conda create -n jupyterlab-ext --override-channels --strict-channel-priority -c conda-forge -c nodefaults jupyterlab=4 nodejs=20 git copier=9 jinja2-time
conda activate jupyterlab-ext

# Build the frontend
./build.sh

pip install -ve .
```

## Development deployment

```bash
# Create sample lab test env
jupyter lab --notebook-dir=.

# Create sample lite test env
jupyter lite build
```
