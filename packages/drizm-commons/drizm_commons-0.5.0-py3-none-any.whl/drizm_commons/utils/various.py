"""
Assortment of uncategorizable utility functions.

````python
from drizm_commons.testing.various import *
````
"""
import re
from typing import Sequence, Mapping, Optional, TypeVar, Callable, Hashable


def camel_to_snake(name: str) -> str:
    """ Converts camelCase names, to snake_case. """
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def exclude_keys(dictionary: Mapping, keys: Sequence[Hashable]) -> dict:
    """
    Removes all key-value pairs, matching the provided keys
    from the dictionary and returns a new one.

    Does not crash when non-existant keys are provided.

    Arguments:
        dictionary: A mapping-type from which keys
            should be removed.
        keys: A sequence of hashable keys to be excluded
            from the new dictionary.

    Returns:
        A new dictionary minus the specified key-value pairs.
    """
    return {k: v for k, v in dictionary.items() if k not in keys}


DecoratedClass = TypeVar("DecoratedClass")


def decorate_class_object_methods(
    cls: DecoratedClass, decorator: Callable, methods: Optional[Sequence[str]] = None
) -> DecoratedClass:
    """
    Programatically decorate all provided attributes of the class,
    with the passed decorator function.

    Arguments:
        cls: The class object to have its methods decorated.
        decorator: The decorator function to be applied to the classes methods.
        methods: A list of attribute names to be decorated.
            Alternatively all non-dunder, instance methods will be decorated.

    Returns:
        The class with its methods decorated.
    """
    from ..testing.truthiness import is_dunder, is_instance_method

    if not methods:
        methods = [
            attr
            for attr in dir(cls)
            if not is_dunder(attr) and is_instance_method(cls, attr)
        ]

    for fn_name in methods:
        fn = getattr(cls, fn_name)
        setattr(cls, fn_name, decorator(fn))

    return cls


__all__ = ["camel_to_snake", "exclude_keys", "decorate_class_object_methods"]
