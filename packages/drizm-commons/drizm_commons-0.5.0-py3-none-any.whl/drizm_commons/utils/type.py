"""
Custom data-type implementations.

````python
from drizm_commons.utils.type import *
````
"""
from typing import TypeVar, Any, Mapping, Optional

DictItem = TypeVar("DictItem")


class AttrDict(dict):
    """
    A dictionary whose keys can be accessed like attributes.

    Example:
        ````python
        obj = AttrDict({
            "test": "ok",
            "something-else": 3
        })
        obj.test  # "ok"
        obj.something_else  # 3
        getattr(obj, "something-else")  # AttributeError
        ````
    """

    __slots__ = []  # override this as to not double `__dict__`

    @staticmethod
    def _keytransform(key: str) -> str:
        """
        Transforms the provided key into an acceptable format,
        for an attribute.
        """
        return key.replace("-", "_").lower()

    def __init__(self, mapping: Optional[Mapping] = (), **kwargs) -> None:
        mapping = {**mapping, **kwargs} if mapping else kwargs

        mapping = dict(
            zip([self._keytransform(k) for k in mapping.keys()], list(mapping.values()))
        )
        super(AttrDict, self).__init__(mapping)

    def __getattr__(self, item: str) -> DictItem:
        try:
            return super(AttrDict, self).__getitem__(item)

        except KeyError:
            # we need to do this so attribute access
            # does not throw a key error
            raise AttributeError from None


class IterableKeyDictionary(dict):
    """
    A dictionary that supports a list or tuple of scalar,
    hashable values as keys.

    Also has support for normal hashable keys.

    Example:
        ````python
        obj = IterableKeyDictionary({
            ("order", 66): "yes my lord"
        })
        obj["order"]  # "yes my lord"
        obj[66]  # "yes my lord"
        obj[("order", 66)]  # "yes my lord"
        ````
    """

    __slots__ = ["__weakref__"]  # add this so the dict can be weakly referenced

    def __getitem__(self, item: Any) -> DictItem:
        if type(item) in (tuple, list):
            return super().__getitem__(item)

        # Try all lists or tuples for the provided key
        for key in [k for k in self.keys() if type(k) in (tuple, list)]:
            if item in key:
                return super().__getitem__(key)

        # If that does not find anything, do the normal key lookup
        return super().__getitem__(item)


__all__ = ["AttrDict", "IterableKeyDictionary"]
