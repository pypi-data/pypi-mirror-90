[![Coverage Status](https://coveralls.io/repos/github/JonatanMartens/eventipy/badge.svg?branch=master)](https://coveralls.io/github/JonatanMartens/eventipy?branch=master)
![Test eventipy](https://github.com/JonatanMartens/eventipy/workflows/test/badge.svg)
![GitHub issues](https://img.shields.io/github/issues-raw/JonatanMartens/eventipy)
![GitHub pull requests](https://img.shields.io/github/issues-pr-raw/JonatanMartens/eventipy)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed-raw/JonatanMartens/eventipy)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/JonatanMartens/eventipy)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/eventipy)
![PyPI](https://img.shields.io/pypi/v/eventipy)


# Eventipy
eventipy is an in-memory event library for python 3.6 and greater.

## Getting Started
To install:

`pip install eventipy`

For full documentation please visit: https://eventipy.readthedocs.io/en/stable/

## Usage

Publishing events:

```python
import asyncio
from eventipy import events, Event

event = Event("my-topic")
asyncio.run(events.publish(event))
```

Subscribing to topics:

```python
from eventipy import events, Event

@events.subscribe("my-topic")
def event_handler(event: Event):
    # Do something with event
    print(event.id)
```

now every time an event with topic `my-topic` is published, `event_handler` will be called.

## Tests
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install eventipy
 
`pytest tests/unit`

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## Versioning
We use [SemVer](semver.org) for versioning. For the versions available, see the tags on this repository.

To bump the version we use [`bumpversion`](https://github.com/c4urself/bump2version) to handle versions. Actions:

Bug fixes:

```shell
$ bumpversion patch # from v1.0.0 -> v1.0.1
```

New features:

```shell
$ bumpversion minor # from v1.0.0 -> v1.1.0
```

Breaking changes:

```shell
$ bumpversion major # from v1.0.0 -> v2.0.0
```

These commands will create a commit, if you want to avoid this please add the `--no-commit` flag.

## License
We use the MIT license, see [LICENSE.md](LICENSE.md) for details
