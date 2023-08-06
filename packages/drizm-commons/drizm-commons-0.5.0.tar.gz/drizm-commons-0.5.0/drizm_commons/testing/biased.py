"""
Contains utilities that are specifically
biased towards certain Drizm organization standards.

````python
from drizm_commons.testing.biased import *
````
"""
from typing import Dict, Union, Optional


def self_to_id(
    body: Dict[str, Union[str, dict]], force_str: Optional[bool] = False
) -> Union[str, int]:
    """
    Extracts the ID from a Drizm-HATEOAS compliant response body.

    Example body:

    ````json
    {
        "self": {"href": "http://example.net/resources/1/"}
    }
    ````

    For the above body, the returned value would be 1.

    Arguments:
        body: The JSONified response body.
        force_str: If `True`, will always output a string,
            the default behaviour is to try and guess the correct type,
            which can be either a String (e.g. UUID),
            or an Integer (Numeric IDs).

    Returns:
        The extracted identifier.
    """
    identifier = [i for i in body["self"].get("href").split("/") if i][-1]
    identifier = [i for i in identifier.split("?") if i][0]

    if not force_str:
        try:
            # Try and convert this into a numeric id
            identifier = int(identifier)

        except TypeError and ValueError:
            # if that fails, we know it must be something like a UUID
            pass

    return identifier


__all__ = ["self_to_id"]
