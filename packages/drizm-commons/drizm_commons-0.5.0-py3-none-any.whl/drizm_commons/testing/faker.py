"""
Utilities for generating randomized test data.

````python
from drizm_commons.testing import faker
````
"""
import io
import random
import string
from typing import Optional, Sequence, Tuple

from PIL import Image


def random_flat_colored_image(
    size_x: int,
    size_y: int,
    ext: Optional[str] = "jpeg",
) -> io.BytesIO:
    """
    Generates a randomized image for testing purposes.

    Arguments:
        size_x: The width of the image to be
            generated, in pixels.
        size_y: The height of the image to be
            generated, in pixels.
        ext: The filetype of the image to be
            generated, e.g. `jpeg` or `png`.

    Returns:
        A BytesIO file object, representing
            the generated image.
    """
    file = io.BytesIO()
    image = Image.new("RGB", size=(size_x, size_y), color=random_rgb_color())
    image.save(file, ext)

    return file


def random_hex_color(short: Optional[bool] = False) -> str:
    """
    Generates a random hexadecimal color string.

    Arguments:
        short: If `True`, this function will generated
            a shortened 3-digit hex color, otherwise a 6-digit
            hex color will be generated instead.

    Returns:
        A three or six digit hex color of the format
            `#ff00ff` or `#f0f`.
    """
    if short:
        return "#%03x" % random.randint(0, 0xFFF)

    return "#%06x" % random.randint(0, 0xFFFFFF)


def random_rgb_color() -> Tuple[int]:
    """
    Generates a random RGB-Color.

    Returns:
        A tuple of 3 integer values between 0 and 255,
            representing the RGB colorspace of the
            generated color.
    """
    return tuple(random.randint(0, 255) for _ in range(3))


def random_email_address(
    top_level_domain: Optional[str] = "com",
    choice_sequence: Optional[Sequence] = string.ascii_lowercase,
) -> str:
    """
    Generates a randomized email address out of provided presets.

    Arguments:
        top_level_domain: The top-level-domain for the email address
            to be generated.
        choice_sequence: A sequence of characters that will be used
            to generated the random host and domain parts of the
            email address.

    Returns:
        A semi-randomized email of the following format: `prefix@host.tld`.
    """
    prefix = "".join(random.choices(choice_sequence, k=12))
    domain = "".join(random.choices(choice_sequence, k=8))
    return f"{prefix}@{domain}.{top_level_domain}"


__all__ = [
    "random_flat_colored_image",
    "random_hex_color",
    "random_rgb_color",
    "random_email_address",
]
