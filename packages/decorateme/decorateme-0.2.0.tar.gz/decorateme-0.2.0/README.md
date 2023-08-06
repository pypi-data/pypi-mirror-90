# Decorate-me

[![Version status](https://img.shields.io/pypi/status/decorateme)](https://pypi.org/project/decorateme/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/decorateme)](https://pypi.org/project/decorateme/)
[![Docker](https://img.shields.io/docker/v/dmyersturnbull/decorate-me?color=green&label=DockerHub)](https://hub.docker.com/repository/docker/dmyersturnbull/decorate-me)
[![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/dmyersturnbull/decorate-me?include_prereleases&label=GitHub)](https://github.com/dmyersturnbull/decorate-me/releases)
[![Latest version on PyPi](https://badge.fury.io/py/decorateme.svg)](https://pypi.org/project/decorateme/)
[![Documentation status](https://readthedocs.org/projects/decorate-me/badge/?version=latest&style=flat-square)](https://decorate-me.readthedocs.io/en/stable/)
[![Build & test](https://github.com/dmyersturnbull/decorate-me/workflows/Build%20&%20test/badge.svg)](https://github.com/dmyersturnbull/decorate-me/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/ce5a27b46cbe0f3c3039/maintainability)](https://codeclimate.com/github/dmyersturnbull/decorate-me/maintainability)
[![Coverage](https://coveralls.io/repos/github/dmyersturnbull/decorate-me/badge.svg?branch=master)](https://coveralls.io/github/dmyersturnbull/decorate-me?branch=master)

Python decorators for str/repr, equality, immutability, and more.

Save lines and document your class’s behavior at the top.
Just `pip install decorateme` and `import decorateme`.


[New issues](https://github.com/dmyersturnbull/decorate-me/issues) and pull requests are welcome.
Please refer to the [contributing guide](https://github.com/dmyersturnbull/decorate-me/blob/master/CONTRIBUTING.md).
Generated with [Tyrannosaurus](https://github.com/dmyersturnbull/tyrannosaurus).


### List of decorators

**String-like methods**
- auto_repr_str
- auto_str
- auto_repr
- auto_html (for display in Jupyter)
- auto_info (add a .info method)

**Equality**
- auto_eq
- auto_hash
- total_ordering  (from functools)

**Make your class smart**
- auto_obj (auto- for eq, str, and repr)
- dataclass (from dataclasses)

**Docstring-related**
- copy_docstring
- append_docstring

**Timing**
- takes_seconds
- takes_seconds_named
- auto_timeout

**Allow a class to be used as a type**
- iterable_over
- collection_over
- sequence_over
- float_type
- int_type

**Overriding / inheritance**
- final
- overrides
- override_recommended
- ABC (from abc)
- ABCMeta  (from abc)
- abstractmethod  (from abc)


**Mark purpose / use**
- internal
- external
- reserved

**Multithreading**
- thread_safe
- not_thread_safe

**Mutability**
- mutable
- immutable

**Code maturity**
- status (code deprecation & immaturity warnings)

**Singletons**
- auto_singleton


Example of `auto_obj` and `float_type`:
```python
import decorateme
@decorateme.auto_obj()
@decorateme.float_type('weight')
class Uno:
    def __init__(self, weight):
        self.weight = weight
print()
light1, light2, heavy = Uno(3.1), Uno(3.1), Uno(12.8)
assert light1 == light2 != heavy
print(light1)  # 'Duo(weight=22.3)'
assert light1 * heavy == 39.68
```
