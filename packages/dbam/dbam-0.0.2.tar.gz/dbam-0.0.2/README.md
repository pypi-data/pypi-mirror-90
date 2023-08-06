# About

`dbam` (short for DataBamboo) is the command line tool for services provided by DataBamboo.com. 

## Installation

You can install `dbam` using `pip`:

```
pip install dbam
```

`dbam` is supported on Python 3.6 and above.

## How to use

run `dbam init` to setup your local environment with API token from DataBamboo.com.

## Test

```bash
pip install pytest
python -m pytest
```

## Packaging and Upload

```
python setup.py sdist
twine upload dist/*
```

