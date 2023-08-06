"""
A collection of decorators.
"""
import enum
import os
import signal
import time
from typing import Optional, Callable, Set, Type
from warnings import warn
from functools import wraps
from abc import abstractmethod, ABC, ABCMeta
from functools import total_ordering
from dataclasses import dataclass


class CodeIncompleteError(NotImplementedError):
    """The code is not finished!"""


class CodeWarning(UserWarning):
    """A warning related to code quality."""


class ObsoleteWarning(CodeWarning, PendingDeprecationWarning):
    """The code being called is obsolete and/or may be deprecated in the future."""


class DeprecatedWarning(CodeWarning, DeprecationWarning):
    """The code being called is deprecated."""


class ImmatureWarning(CodeWarning):
    """The code being called is unstable or immature."""


@enum.unique
class CodeStatus(enum.Enum):
    """
    An enum for the quality/maturity of code,
    ranging from incomplete to deprecated.
    """

    Incomplete = 0
    Immature = 1
    Preview = 2
    Stable = 3
    Obsolete = 4
    Deprecated = 5


class _SpecialStr(str):
    """
    A string that can be displayed with Jupyter with line breaks and tabs.
    """

    def __init__(self, s: str):
        super().__init__()
        self.s = str(s)

    def __repr__(self):
        return repr(self.s)

    def __str__(self):
        return str(self.s)

    def _repr_html_(self):
        return str(self.s.replace("\n", "<br />").replace("\t", "&emsp;&emsp;&emsp;&emsp;"))


class _InfoSpecialStr(_SpecialStr):
    def _repr_html_(self):
        if len(self.s) == 0:
            return self.s
        lines = self.s.split("\n")
        built = "<strong>" + lines[0] + "</strong><br/>\n"
        if len(lines) > 1:
            for line in lines[1:-1]:
                if "=" in line:
                    k, v = line[: line.index("=")], line[line.index("=") :]
                    built += "&emsp;&emsp;&emsp;&emsp;<strong>" + k + "</strong>" + v + "<br/>\n"
                else:
                    built += line + "<br />\n"
        built += "<strong>)</strong>\n"
        return str(built)


class _Utils:
    def gen_str(
        self,
        only: Optional[Set[str]] = None,
        exclude: Optional[Callable[[str], bool]] = None,
        bold_surround: Callable[[str], str] = str,
        em_surround: Callable[[str], str] = str,
        delim: str = ", ",
        eq: str = "=",
        opening: str = "(",
        closing: str = ")",
        with_address: bool = True,
    ):
        if exclude is None:
            exclude = lambda _: False
        _vars = _Utils.var_items(self, only, exclude)
        return (
            bold_surround(self.__class__.__name__)
            + opening
            + delim.join([k + eq + str(v) for k, v in _vars])
            + em_surround(" @ " + str(hex(id(self))) if with_address else "")
            + closing
        )

    @classmethod
    def var_items(cls, obj, only, exclude):
        return [
            (key, value)
            for key, value in vars(obj).items()
            if (only is None) or (key in only)
            if not exclude(key)
        ]

    @classmethod
    def var_values(cls, obj, only, exclude):
        items = vars(obj).items()
        return [
            value
            for key, value in items
            if ((only is None) or key in only) and not exclude(key) and value is not None
        ]

    @classmethod
    def auto_hash(cls, self, only: Optional[Set[str]], exclude: Optional[Callable[[str], bool]]):
        if exclude is None:
            exclude = lambda _: False
        return hash(tuple(_Utils.var_values(self, only, exclude)))

    @classmethod
    def auto_eq(
        cls,
        self,
        other,
        only: Optional[Set[str]],
        exclude: Optional[Callable[[str], bool]],
    ):
        if type(self) != type(other):
            raise TypeError("Type {} is not the same as type {}".format(type(self), type(other)))
        if exclude is None:
            exclude = lambda _: False
        return _Utils.var_values(self, only=only, exclude=exclude) == _Utils.var_values(
            other, only, exclude
        )


def auto_eq(only: Optional[Set[str]] = None, exclude: Optional[Callable[[str], bool]] = None):
    """
    Decorator. Auto-adds a __eq__ function by comparing its attributes.

    Args:
        only: Only include these attributes
        exclude: Exclude these attributes
    """

    @wraps(auto_eq)
    def dec(cls):
        def __eq(self, other):
            return _Utils.auto_eq(self, other, only, exclude)

        cls.__eq__ = __eq
        return cls

    return dec


def auto_hash(only: Optional[Set[str]] = None, exclude: Optional[Callable[[str], bool]] = None):
    """
    Decorator. Auto-adds a __hash__ function by hashing its attributes.

    Args:
        only: Only include these attributes
        exclude: Exclude these attributes
    """

    @wraps(auto_hash)
    def dec(cls):
        def __hash(self):
            return _Utils.auto_hash(self, only, exclude)

        cls.__hash__ = __hash
        return cls

    return dec


def auto_repr(
    only: Optional[Set[str]] = None,
    exclude: Optional[Callable[[str], bool]] = lambda a: False,
):
    """
    Decorator. Auto-adds __repr__ and __str__.

    Args:
        only: Only include these attributes
        exclude: Exclude these attributes
    """

    @wraps(auto_repr)
    def dec(cls):
        def __repr(self):
            return _Utils.gen_str(self, only=only, exclude=exclude, with_address=True)

        cls.__repr__ = __repr
        return cls

    return dec


def auto_str(
    only: Optional[Set[str]] = None,
    exclude: Optional[Callable[[str], bool]] = lambda a: a.startswith("_"),
    with_address: bool = False,
):
    """
    Decorator. Auto-adds __str__.

    Args:
        only: Only include these attributes
        exclude: Exclude these attributes
        with_address: Include the hex memory address
    """

    @wraps(auto_str)
    def dec(cls):
        def __str(self):
            return _Utils.gen_str(self, only=only, exclude=exclude, with_address=with_address)

        cls.__str__ = __str
        return cls

    return dec


def auto_html(
    only: Optional[Set[str]] = None,
    exclude: Optional[Callable[[str], bool]] = lambda a: lambda b: b.startswith("_"),
    with_address: bool = True,
):
    """
    Decorator. Auto-adds a ``_repr_html`` method, which Jupyter will use.

    Args:
        only: Only include these attributes
        exclude: Exclude these attributes
        with_address: Include the hex memory address
    """

    @wraps(auto_html)
    def dec(cls):
        def __html(self):
            return _SpecialStr(
                _Utils.gen_str(
                    self,
                    only=only,
                    exclude=exclude,
                    with_address=with_address,
                    bold_surround=lambda c: "<strong>" + c + "</strong>",
                    em_surround=lambda c: "<em>" + c + "</em>",
                )
            )

        cls._repr_html = __html
        return cls

    return dec


def auto_repr_str(
    exclude_simple: Optional[Callable[[str], bool]] = lambda a: a.startswith("_"),
    exclude_html: Optional[Callable[[str], bool]] = lambda a: a.startswith("_"),
    exclude_all: Optional[Callable[[str], bool]] = lambda a: False,
):
    """
    Decorator.
    Auto-adds __repr__, __str__, and _repr_html that show the attributes:
        - __str__ will include attributes in neither exclude_all nor exclude_simple
        - _repr_html_ will include attributes in neither exclude_all nor exclude_simple
            and will show the hexadecimal address
        - __repr__ will include attributes not in exclude_all and will show the hexadecimal address

    The _repr_html_ will be used by Jupyter display.

    Examples:
        - ``repr(point) == Point(angle=0.3, radius=4, _style='point' @ 0x5528ca3)``
        - ``str(point) == Point(angle=0.3, radius=4)``
        - ``_repr_html_(point) == Point(angle=0.3, radius=4 @ 0x5528ca3)``

    Args:
        exclude_simple: Exclude attributes matching these names in human-readable strings (str and _repr_html)
        exclude_html: Exclude for _repr_html
        exclude_all: Exclude these attributes in all the functions
    """

    @wraps(auto_repr_str)
    def dec(cls):
        def __str(self):
            return _Utils.gen_str(self, only=None, exclude=exclude_simple, with_address=False)

        def __html(self):
            return _SpecialStr(
                _Utils.gen_str(
                    self,
                    only=None,
                    exclude=exclude_html,
                    with_address=True,
                    bold_surround=lambda c: "<strong>" + c + "</strong>",
                    em_surround=lambda c: "<em>" + c + "</em>",
                )
            )

        def __repr(self):
            return _Utils.gen_str(self, only=None, exclude=exclude_all, with_address=True)

        cls.__str__ = __str
        cls.__repr__ = __repr
        cls._repr_html_ = __html
        return cls

    return dec


def auto_info(
    only: Optional[Set[str]] = None,
    exclude: Optional[Callable[[str], bool]] = lambda a: a.startswith("_"),
):
    """
    Decorator. Auto-adds a function ``info`` that outputs a pretty multi-line representation of the instance and its attributes.

    Args:
        only: Only include these attributes
        exclude: Exclude these attributes
    """

    @wraps(auto_info)
    def dec(cls):
        def __info(self):
            return _InfoSpecialStr(
                _Utils.gen_str(
                    self,
                    delim="\n\t",
                    eq=" = ",
                    opening="(\n\t",
                    closing="\n)",
                    with_address=False,
                    only=only,
                    exclude=exclude,
                )
            )

        cls.info = __info
        return cls

    return dec


def auto_obj():
    """
    Auto-adds ``__eq__``, ``__hash__``, ``__repr__``, ``__str__``, and ``_repr_html``.
    See the decorators for auto_eq, auto_hash, and auto_repr for more details.
    """

    def __str(self):
        return _Utils.gen_str(self, exclude=lambda a: a.startswith("_"), with_address=False)

    def __html(self):
        return _SpecialStr(
            _Utils.gen_str(
                self,
                only=None,
                exclude=lambda a: a.startswith("_"),
                with_address=True,
                bold_surround=lambda c: "<strong>" + c + "</strong>",
            )
        )

    def __repr(self):
        return _Utils.gen_str(self, exclude=lambda _: False, with_address=True)

    def __hash(self):
        return _Utils.auto_hash(self, only=None, exclude=None)

    def __eq(self, o):
        return _Utils.auto_eq(self, o, only=None, exclude=None)

    @wraps(auto_obj)
    def dec(cls):
        cls.__eq__ = __eq
        cls.__str__ = __str
        cls.__repr__ = __repr
        cls.__hash__ = __hash
        cls._repr_html_ = __html
        return cls

    return dec


def takes_seconds_named(x, *args, **kwargs):
    """
    Decorator. Prints a statement like "Call to calc_distances took 15.2s." after the function returns.
    """
    t0 = time.monotonic()
    results = x(*args, **kwargs)
    print("Call to {} took {}s.".format(x.__name__, round(time.monotonic() - t0, 1)))
    return results


def takes_seconds(x, *args, **kwargs):
    """
    Decorator. Prints a statement like "Done. Took 15.2s." after the function returns.
    """
    t0 = time.monotonic()
    results = x(*args, **kwargs)
    print("Done. Took {}s.".format(round(time.monotonic() - t0, 1)))
    return results


def mutable(cls):
    """
    Decorator. Just marks an object as mutable.
    """
    return cls


def immutable(mutableclass):
    """
    Decorator for making a slot-based class immutable.
    Taken almost verbatim from https://code.activestate.com/recipes/578233-immutable-class-decorator/
    Written by Oren Tirosh and released under the MIT license.
    """
    if not isinstance(type(mutableclass), type):
        raise TypeError("@immutable: must be applied to a new-style class")
    if not hasattr(mutableclass, "__slots__"):
        raise TypeError("@immutable: class must have __slots__")

    # noinspection PyPep8Naming
    class immutableclass(mutableclass):
        __slots__ = ()  # No __dict__, please

        def __new__(cls, *args, **kw):
            new = mutableclass(*args, **kw)  # __init__ gets called while still mutable
            new.__class__ = immutableclass  # locked for writing now
            return new

        def __init__(self, *args, **kw):  # Prevent re-init after __new__
            pass

    # Copy class identity:
    immutableclass.__name__ = mutableclass.__name__
    immutableclass.__module__ = mutableclass.__module__
    # Make read-only:
    for name, member in mutableclass.__dict__.items():
        if hasattr(member, "__set__"):
            setattr(immutableclass, name, property(member.__get__))
    return immutableclass


def copy_docstring(from_obj: Type):
    """
    Decorator. Copies the docstring from `from_obj` to this function or class.
    """

    @wraps(copy_docstring)
    def dec(myobj):
        myobj.__doc__ = from_obj.__doc__
        return myobj

    return dec


def append_docstring(from_obj: Type):
    """
    Decorator. Appends the docstring from `from_obj` to the docstring for this function or class.
    """

    @wraps(append_docstring)
    def dec(myobj):
        myobj.__doc__ += from_obj.__doc__
        return myobj

    return dec


def float_type(attribute: str):
    """
    Decorator. Auto-adds a ``__float__`` using the ``__float__`` of some attribute.
    Used to annotate a class as being "essentially an float".

    Args:
        attribute: The name of the attribute of this class
    """

    def __f(self):
        return float(getattr(self, attribute))

    @wraps(float_type)
    def dec(cls):
        cls.__float__ = __f
        return cls

    return dec


def int_type(attribute: str):
    """
    Decorator. Auto-adds an ``__int__`` using the ``__int__`` of some attribute.
    Used to annotate a class as being "essentially an integer".

    Args:
        attribute: The name of the attribute of this class
    """

    def __f(self):
        return float(getattr(self, attribute))

    def __i(self):
        return float(getattr(self, attribute))

    @wraps(int_type)
    def dec(cls):
        cls.__float__ = __f
        cls.__int__ = __i
        return cls

    return dec


def iterable_over(attribute: str):
    """
    Decorator. Auto-adds an ``__iter__`` over elements in an iterable attribute.
    Used to annotate a class as being "essentially an iterable" over some elements.

    Args:
        attribute: The name of the attribute of this class
    """

    def __x(self):
        return iter(getattr(self, attribute))

    @wraps(iterable_over)
    def dec(cls):
        cls.__iter__ = __x
        return cls

    return dec


def collection_over(attribute: str):
    """
    Decorator. Auto-adds an ``__iter__`` and ``__len__`` over elements in a collection attribute.
    Used to annotate a class as being "essentially a collection" over some elements.

    Args:
        attribute: The name of the attribute of this class
    """

    def __len(self):
        return len(list(iter(getattr(self, attribute))))

    def __iter(self):
        return iter(getattr(self, attribute))

    @wraps(collection_over)
    def dec(cls):
        cls.__iter__ = __iter
        cls.__len__ = __len
        return cls

    return dec


def sequence_over(attribute: str):
    """
    Decorator. Auto-adds ``__getitem__`` and ``__len__`` over elements in an iterable attribute.
    Used to annotate a class as being "essentially a list" over some elements.

    Args:
        attribute: The name of the attribute of this class
    """

    def __len(self):
        return len(list(iter(getattr(self, attribute))))

    def __iter(self):
        return iter(getattr(self, attribute))

    def __item(self, e):
        if hasattr(getattr(self, attribute), "__getitem__"):
            return getattr(self, attribute)[e]
        return iter(getattr(self, attribute))

    @wraps(sequence_over)
    def dec(cls):
        cls.__getitem__ = __item
        cls.__iter__ = __iter
        cls.__len__ = __len
        return cls

    return dec


def auto_singleton(cls):
    """
    Makes it so the constructor returns a singleton instance.
    The constructor CANNOT take arguments.
    Example usage:
    >>> @auto_singleton
    >>> class MyClass: pass
    >>> mysingleton = MyClass()
    """
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance


def status(level: CodeStatus):
    """
    Decorator. Annotate code quality. Emits a warning if bad code is called.

    Args:
        level: The quality / maturity as an enum
    """

    @wraps(status)
    def dec(func):
        func.__status__ = level
        if level in [CodeStatus.Preview, CodeStatus.Stable]:
            return func
        elif level == CodeStatus.Incomplete:

            def my_fn(*args, **kwargs):
                raise CodeIncompleteError(str(func.__name__) + " is incomplete!")

            return wraps(func)(my_fn)
        elif level == CodeStatus.Immature:

            def my_fn(*args, **kwargs):
                warn(str(func.__name__) + " is immature", ImmatureWarning)
                return func(*args, **kwargs)

            return wraps(func)(my_fn)
        elif level == CodeStatus.Obsolete:

            def my_fn(*args, **kwargs):
                warn(str(func.__name__) + " is obsolete", ObsoleteWarning)
                return func(*args, **kwargs)

            return wraps(func)(my_fn)
        elif level == CodeStatus.Deprecated:

            def my_fn(*args, **kwargs):
                warn(str(func.__name__) + " is deprecated", DeprecatedWarning)
                return func(*args, **kwargs)

            return wraps(func)(my_fn)
        raise AssertionError(f"What is {level}?")

    return dec


@status(CodeStatus.Immature)
def auto_timeout(seconds: int):
    """
    Decorator. The decorated function will be subject to a timeout of ``seconds``.
    If it takes longer than that, it will raise a ``TimeoutError``.

    Note::

        Uses ``signal.alarm`` for interruption.

    Raises:
        NotImplementedError: If running on Windows
        TimeoutError: The call took too long
    """
    if os.name.lower() == "nt":
        raise NotImplementedError("Cannot use @auto_timeout on Windows")

    @wraps(auto_timeout)
    def dec(func):
        def _handle_timeout(the_signal, the_frame):
            raise TimeoutError(f"The call timed out after {seconds} s")

        def my_fn(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(my_fn)

    return dec


def overrides(cls):
    """
    Decorator. Overriding this class is generally recommended (but not required).
    """
    return cls


def override_recommended(cls):
    """
    Decorator. Overriding this class is suggested.
    """
    return cls


def internal(cls):
    """
    Decorator. This class or package is meant to be used only by code within this project.
    """
    return cls


def external(cls):
    """
    Decorator. This class or package is meant to be used *only* by code outside this project.
    """
    return cls


def reserved(cls):
    """
    Decorator. This package, class, or function is empty but is declared for future use.
    """
    return cls


def thread_safe(cls):
    """
    Decorator. Just marks that something **is** thread-safe.
    """
    return cls


def not_thread_safe(cls):
    """
    Decorator. Just marks that something is **not** thread-safe.
    """
    return cls


def final(cls):
    """
    Decorator. Marks as "should not override".
    """
    return cls


__all__ = [
    "dataclass",
    "final",
    "auto_repr_str",
    "auto_str",
    "auto_repr",
    "auto_html",
    "auto_info",
    "auto_eq",
    "auto_hash",
    "total_ordering",
    "auto_obj",
    "copy_docstring",
    "append_docstring",
    "auto_singleton",
    "takes_seconds",
    "takes_seconds_named",
    "auto_timeout",
    "mutable",
    "immutable",
    "iterable_over",
    "collection_over",
    "sequence_over",
    "float_type",
    "int_type",
    "abstractmethod",
    "ABC",
    "ABCMeta",
    "override_recommended",
    "overrides",
    "internal",
    "external",
    "reserved",
    "thread_safe",
    "not_thread_safe",
    "CodeStatus",
    "CodeWarning",
    "CodeIncompleteError",
    "DeprecatedWarning",
    "ObsoleteWarning",
    "ImmatureWarning",
]
