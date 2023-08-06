"""
Contains utilities for the conversion of data.

````python
from drizm_commons.testing.conversion import *
````
"""
import base64
import io


def image_file_to_b64(image_file: io.BytesIO) -> bytes:
    """
    Encodes an image file as Base64.

    To obtain the stringified Base64 version of the image,
    you can convert the output like so:

    ````python
    image_file_to_b64(my_image_file).decode()
    ````

    Arguments:
        image_file: The BytesIO file object to be converted.

    Returns:
        Bytes representation of the Base64 encoded image.
    """
    return base64.b64encode(image_file.getvalue())


__all__ = ["image_file_to_b64"]
