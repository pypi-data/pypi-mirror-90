# Changes

All notable changes to this project will be documented in this file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v1.0.0] - 2021-01-08

### Added

- Packaging: new prerequisite "jomiel-comm"
- Packaging: new prerequisite "jomiel-kore"

### Changed

- Repository doesn't have git-subtrees anymore

### Removed

- `jomiel-comm` and `jomiel-kore` from the subtrees

## [v0.999] - 2020-09-15

- Packaging: new prerequisite "jomiel-messages"
- Packaging: modernize setup with PEP-517+518

### Changed

- Use src/ layout from now on

### Removed

- jomiel-proto from the subtrees, don't dist `*_pb2.py` anymore
- requirements.[txt,in], use setup.cfg and `install_requires`

## [v0.5.1] - 2020-06-25

### Added

- Packaging: new prerequisite "ujson"

### Changed

- Regenerate pinned package requirements

## [v0.5.0] - 2020-05-16

### Changed

- Reformat code according to pre-commit (with added) hooks
- Regenerate pinned package requirements

## [v0.4.0] - 2020-02-02

### Added

- Packaging: new prerequisite "importlib-resources"
- Packaging: new prerequisite "importlib-metadata"
- yomiel/data package

### Changed

- Use restructured .proto files (jomiel-proto)
- Regenerate pinned package requirements
- yomiel now requires py36+

## [v0.2.0] - 2019-11-25

### Added

- pre-commit files
- tox files

### Changed

- Use black, instead of yapf, for code formatting from now on
- Packaging: bump all requirements to their latests

## [v0.1.2] - 2019-10-28

### Changed

- Use new default port value "5514" for broker router
- Packaging: use pip-compile for pinning packages
- Documentation: replace animated `*.png` files with a single .svg

## [v0.1.1] - 2019-09-30

### Added

- --output-format: now supports "terse" output
- --logger-idents-verbose option

### Changed

- Enable input URI validation
- Packaging: bump requirements (protobuf, ruamel.yaml, pyzmq)
- Packaging: produce py3-only dist packages from now on

### Fixed

- --logger-idents: now fully implemented

## [v0.1.0] - 2019-08-05

- First public preview release.

[unreleased]: https://github.com/guendto/jomiel-yomiel/compare/v1.0.0..HEAD
[v1.0.0]: https://github.com/guendto/jomiel-yomiel/compare/v0.999..v1.0.0
[v0.999]: https://github.com/guendto/jomiel-yomiel/compare/v0.5.0..v0.999
[v0.5.1]: https://github.com/guendto/jomiel-yomiel/compare/v0.5.0..v0.5.1
[v0.5.0]: https://github.com/guendto/jomiel-yomiel/compare/v0.4.0..v0.5.0
[v0.4.0]: https://github.com/guendto/jomiel-yomiel/compare/v0.2.0..v0.4.0
[v0.2.0]: https://github.com/guendto/jomiel-yomiel/compare/v0.1.2..v0.2.0
[v0.1.2]: https://github.com/guendto/jomiel-yomiel/compare/v0.1.1..v0.1.2
[v0.1.1]: https://github.com/guendto/jomiel-yomiel/compare/v0.1.0..v0.1.1
[v0.1.0]: https://github.com/guendto/jomiel-yomiel/releases/tag/v0.1.0
