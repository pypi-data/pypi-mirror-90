# AIS-api [![Build Status][travis_status]][travis] [![PyPI version][pypi_badge]][pypi]

_Python wrapper package for the AIS API._

## Install

```bash
pip install ais-api
```

Look at the file `example.py` for a usage example.

[travis_status]: https://travis-ci.org/sviete/ais-api.svg?branch=master
[travis]: https://travis-ci.org/sviete/ais-api
[pypi]:https://pypi.org/project/ais-api/
[pypi_badge]: https://badge.fury.io/py/ais-api.svg


## Develop


## Publish the new version to pip

```bash
rm -rf dist
python3 setup.py sdist bdist_wheel
twine upload dist/*
```
