# Changes

All notable changes to this project will be documented in this file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v1.0.0] - 2021-01-08

### Added

- Packaging: new prerequisite [jomiel-comm]
- Packaging: new prerequisite [jomiel-kore]

[jomiel-comm]: https://pypi.org/project/jomiel-comm
[jomiel-kore]: https://pypi.org/project/jomiel-kore

### Removed

- git-subtrees for `jomiel-comm` and `jomiel-kore`

## [v0.999] - 2020-09-14

### Added

- Documentation/HOWTO: "build a release from the repo"
- Packaging: new prerequisite "jomiel-messages"
- Packaging: modernize setup with PEP-517+518

### Changed

- Use src/ layout from now on

### Removed

- jomiel-proto from the subtrees, don't dist `*_pb2.py` anymore
- requirements.[txt,in], use setup.cfg and `install_requires`

## [v0.4.2] - 2020-07-27

### Added

- Document: `jomiel` is a spiritual successor to libquvi

## [v0.4.1] - 2020-06-25

### Added

- Packaging: new prerequisite "ujson"

### Changed

- Use "ujson" instead of "json" package for improved performance
- Regenerate pinned package requirements

## [v0.4.0] - 2020-05-16

### Changed

- Reformat code according to pre-commit (with added) hooks
- Regenerate pinned package requirements

## [v0.3.0] - 2020-03-17

### Added

- Packaging: new prerequisite "importlib-resources"
- jomiel/data package

### Changed

- jomiel-keygen: disable --print-config (redundant)
- Use restructured .proto files (jomiel-proto)
- Regenerate pinned package requirements

### Fixed

- jomiel-keygen: output filename arg count check (9939599)

## [v0.2.1] - 2019-12-20

### Added

- Packaging: new prerequisite "importlib-metadata"

### Changed

- Use importlib-metadata for querying package metadata
- Make improvements to plugin.media.youtube.parser
- Regenerate pinned package requirements
- jomiel now requires py36+

### Fixed

- plugin.media.youtube.parser: skip token check if none is found

## [v0.2.0] - 2019-11-11

### Added

- pre-commit files
- tox files

### Changed

- Use black, instead of yapf, for code formatting from now on
- Reformat code according to pre-commit hooks

## [v0.1.3] - 2019-11-01

### Changed

- Use "Invalid input URI value given" for InvalidInputError
- Use new default port value "5514" for broker router
- Documentation: replace animated `*.png` files with a single .svg
- Packaging: bump requirements (protobuf, configargparse)
- Packaging: use pip-compile for pinning packages

## [v0.1.2] - 2019-09-30

### Added

- --broker-input-allow-any option
- Packaging: new prerequisite "validators"

### Changed

- Validate the value of incoming "input URL" by default from now on
- Packaging: bump requirements (protobuf, pyzmq, ruamel.yaml)

## [v0.1.1] - 2019-08-29

### Added

- --logger-idents-verbose option
- README.md: add HOWTO

### Changed

- --plugin-list no longer print redundant (info-level) messages
- --plugin-list now prints in the yaml format
- Packaging: bump requirements (protobuf, pyzmq, ruamel.yaml)
- Packaging: produce py3-only dist packages from now on

### Fixed

- plugin/media/youtube/parser: "KeyError: 'videoDetails'"
- plugin/media/youtube/parser: "KeyError: 'title'"

## [v0.1.0] - 2019-07-30

- First public preview release.

[unreleased]: https://github.com/guendto/jomiel/compare/v1.0.0...HEAD
[v1.0.0]: https://github.com/guendto/jomiel/compare/v0.999...v1.0.0
[v0.999]: https://github.com/guendto/jomiel/compare/v0.4.2...v0.999
[v0.4.2]: https://github.com/guendto/jomiel/compare/v0.4.1...v0.4.2
[v0.4.1]: https://github.com/guendto/jomiel/compare/v0.4.0...v0.4.1
[v0.4.0]: https://github.com/guendto/jomiel/compare/v0.3.0...v0.4.0
[v0.3.0]: https://github.com/guendto/jomiel/compare/v0.2.1...v0.3.0
[v0.2.1]: https://github.com/guendto/jomiel/compare/v0.2.0...v0.2.1
[v0.2.0]: https://github.com/guendto/jomiel/compare/v0.1.3...v0.2.0
[v0.1.3]: https://github.com/guendto/jomiel/compare/v0.1.2...v0.1.3
[v0.1.2]: https://github.com/guendto/jomiel/compare/v0.1.1...v0.1.2
[v0.1.1]: https://github.com/guendto/jomiel/compare/v0.1.0...v0.1.1
[v0.1.0]: https://github.com/guendto/jomiel/releases/tag/v0.1.0
