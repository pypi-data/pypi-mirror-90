# yomiel

[![pypi-pyversions](https://img.shields.io/pypi/pyversions/yomiel?color=%230a66dc)][pypi]
[![pypi-v](https://img.shields.io/pypi/v/yomiel?color=%230a66dc)][pypi]
[![pypi-wheel](https://img.shields.io/pypi/wheel/yomiel?color=%230a66dc)][pypi]
[![pypi-status](https://img.shields.io/pypi/status/yomiel?color=%230a66dc)][pypi]
[![code-style](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi]: https://pypi.org/project/yomiel
[black]: https://pypi.org/project/black

`yomiel` is the pretty printer for [jomiel] messages.

![Example (yomiel)](./docs/demo.svg)

## Features

- Support for different output formats (raw/json/yaml)
- Authentication and encryption ([CURVE] and [SSH])
- Highly configurable

## Getting started

- `yomiel` requires [Python] 3.6+
- Make sure `jomiel` is running

To install from [PyPI]:

```shell
pip install yomiel
```

To run from the repository:

```shell
git clone https://github.com/guendto/jomiel-yomiel.git
cd jomiel-yomiel
pip install -e .
```

Be sure to check out `jomiel` [HOWTO], also.

## License

`yomiel` is licensed under the [Apache License version 2.0][aplv2].

## Acknowledgements

`yomiel` uses [pre-commit] and its many hooks to lint and format the
project files. See the .pre-commit-config.yaml file for details.

[python]: https://www.python.org/about/gettingstarted/
[howto]: https://github.com/guendto/jomiel/blob/master/docs/HOWTO.md#howto-jomiel
[jomiel]: https://github.com/guendto/jomiel/
[aplv2]: https://www.tldrlegal.com/l/apache2
[ssh]: https://en.wikipedia.org/wiki/Ssh
[pre-commit]: https://pre-commit.com/
[curve]: http://curvezmq.org/
[pypi]: https://pypi.org/
