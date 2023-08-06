"""
Contains utilities to check for the
truthiness of assertions.

````python
from drizm_commons.testing.truthiness import *
````
"""
import inspect
from typing import Optional, Hashable, Dict, Any, Sequence
from urllib.parse import urlparse
from uuid import UUID


def all_keys_present(
    dictionary: Dict[Hashable, Any],
    keys: Sequence[Hashable],
    strict: Optional[bool] = False,
) -> bool:
    """
    Checks whether all provided keys are present in the dictionary.

    Arguments:
        dictionary: The dictionary to be checked.
        keys: A sequence of hashable values to be searched for.
            Must not contain any duplicate values.
        strict: If `True`, this will check that the provided
            keys 1:1 match the keys in the dictionary.

    Returns:
        `True` if all provided keys were found in the dictionary,
            `False` otherwise.
    """
    if not strict:
        return all(k in dictionary.keys() for k in keys)

    else:
        return set(dictionary.keys()) == set(keys)


def all_items_present(sequence: Sequence[Hashable], values: Sequence[Hashable]) -> bool:
    """
    Check whether all provided `values` are present at any index
    in the provided `sequence`.

    Arguments:
        sequence: An iterable of Hashable values to check for values in.
        values: An iterable of Hashable values for whose presence to
            check `sequence` for.

    Returns:
        `True` if all `values` are present somewhere in `sequence`,
            else `False`.
    """
    return all(k in sequence for k in values)


def uri_is_http(uri: str) -> bool:
    """
    Check whether a string is a valid HTTP URI.

    Arguments:
        uri: The string to check.

    Returns:
        `True` if the string is a valid URI, `False` otherwise.
    """
    if uri.startswith("http") or uri.startswith("https"):
        try:
            result = urlparse(uri)
            return all([result.scheme, result.netloc, result.path])

        except AttributeError or TypeError:
            return False

    return False


def is_dunder(name: str) -> bool:
    """
    Check whether a given attribute name
    is a dunder, e.g. `__name__`.

    Arguments:
        name: The provided attribute name.

    Returns:
        `True` if `name` is a valid dunder, else `False`.
    """
    if (name[:2] and name[-2:]) in ("__",):
        return True

    return False


def all_items_equal(sequence: Sequence[Hashable]) -> bool:
    """
    Check whether all hashable items in a sequence are equal.

    Arguments:
        sequence: A sequence of hashables to be checked.

    Returns:
        `True` if all items in the sequence are equal, else `False`.
    """
    if isinstance(sequence, Sequence):
        return len(set(sequence)) == 1

    raise TypeError("Only list and tuples may be processed")


def all_nested_zipped_equal(sequence: Sequence[Sequence]) -> bool:
    """
    Check whether all items, at the same indexes,
    in a nested sequence are equal.

    For example:

    ````python
    example_list = [[1, 2], [1, 2], [1, 2]]
    all_nested_zipped_equal(example_list)
    ````

    Is the same as:
    ````python
    example_list[0][0] == example_list[1][0] == example_list[2][0]
    ````

    Arguments:
        sequence: A nested sequence to be checked.

    Returns:
        `True` if the contents of the nested
            sequences are equal, else `False`.
    """
    return all([all_items_equal(subiter) for subiter in zip(*sequence)])


def uuid4_is_valid(value: str) -> bool:
    """
    Check whether a given string is a valid UUIDv4.

    Arguments:
        value: The string to be tested.

    Returns:
        `True` if the string is a valid UUIDv4, else `False`.
    """
    try:
        val = UUID(value, version=4)

    except ValueError:
        return False

    return val.hex == value


def is_class_method(klass, name: str) -> bool:
    """
    Check if the attribute of the passed `klass`
    is a `@classmethod`.

    This is a strict check, meaning it actually checks for the
    `@classmethod` descriptor.

    Credit for this implementation goes to:
    https://stackoverflow.com/a/19228282`.

    Arguments:
        klass: Class object or instance to check for the attribute on.
        name: Name of the attribute to check for.

    Returns:
        `True` if the method is a classmethod, else `False`.
    """
    if not inspect.isclass(klass):
        klass = klass.__class__

    meth = getattr(klass, name)

    if inspect.isfunction(meth):
        if getattr(meth, "__self__", None):
            return True

    for cls in klass.__mro__:
        descriptor = vars(cls).get(name)
        if descriptor is not None:
            return isinstance(descriptor, classmethod)


def is_instance_method(klass, name: str) -> bool:
    """
    Check if the attribute of the passed `klass`
    is an instance method.

    Arguments:
        klass: Class object or instance to check for the attribute on.
        name: Name of the attribute to check for.

    Returns:
        `True` if the method is an instance method, else `False`.
    """
    if not inspect.isclass(klass):
        klass = klass.__class__

    meth = getattr(klass, name)

    # Check that it is actually a function, not an attribute
    if inspect.isfunction(meth):
        # Instance methods would only be bound to an instance,
        # not a class
        if getattr(meth, "__self__", None):
            return False

        if is_static_method(klass, name):
            return False

        return True


def is_static_method(klass, name: str) -> bool:
    """
    Check if the attribute of the passed `klass`
    is a `@staticmethod`.

    Arguments:
        klass: Class object or instance to check for the attribute on.
        name: Name of the attribute to check for.

    Returns:
        `True` if the method is a staticmethod, else `False`.
    """
    if not inspect.isclass(klass):
        klass = klass.__class__

    meth = getattr(klass, name)

    if inspect.isfunction(meth):
        if getattr(meth, "__self__", None):
            return False

    for cls in klass.__mro__:
        descriptor = vars(cls).get(name)
        if descriptor is not None:
            return isinstance(descriptor, staticmethod)

    return False


__all__ = [
    "all_items_equal",
    "all_items_present",
    "all_nested_zipped_equal",
    "all_keys_present",
    "uuid4_is_valid",
    "uri_is_http",
    "is_dunder",
    "is_class_method",
    "is_static_method",
    "is_instance_method",
]
