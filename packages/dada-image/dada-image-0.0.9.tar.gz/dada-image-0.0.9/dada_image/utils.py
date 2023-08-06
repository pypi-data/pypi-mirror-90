"""
Utilities for parsing and generating images
TODO
    - Image quilting
"""
# ///////////////////
# Imports
# ///////////////////

import io
import base64
import hashlib
import logging
from typing import List, Union, Optional, Callable, NewType

from colorthief import ColorThief
from PIL import Image, ImageDraw

from dada_utils import path

# ///////////////////
# Logger
# ///////////////////

DATA_IMAGE_LOGGER = logging.getLogger()

# /////////////
# Custom Types
# /////////////

ImgColor = NewType(
    "ImgColor", Union[str, List[int]]
)  # either  "#F4F4F4" or (244, 244, 244)
ImgFilepath = NewType(
    "ImgFilepath", Union[str, Image]
)  # union of filepath / Image objec
# we do this so we can chain PIL functions together and not write to/from file every time.

# ///////////////////
# Reusable Doc Strings
# ///////////////////

IMG_PARAM = ":param img: A PIL.Image or a filepath containing an image"
FORMAT_PARAM = (
    ":param format: The format to write the image as (either ``PNG`` or ``JPEG``)"
)
THUMB_SIZE_PARAM = (
    ":param size: The dimension of thumbnail to generate (eg: 640 -> (640, 640))"
)
OUT_FILEPATH_PARAM = ":param filepath: an optional filepath to write to, if not provided a tempfile will be created."
WIDTH_PARAM = ":param width: The desired width."
HEIGHT_PARAM = ":param width: The desired height."

# ///////////////////
# FUNCTIONS
# ///////////////////


def from_filepath(img: ImgFilepath, **kwargs: dict) -> Image:
    f"""
    Load an image from a filepath or passthrough an existing PIL image
    {IMG_PARAM}
    :return PIL.Image
    """
    if isinstance(img, Image):
        return img
    return Image.open(img)


def get_aspect_ratio(img: ImgFilepath) -> float:
    f"""
    Get the aspect ratio on an image
    {IMG_PARAM}
    :return float
    """
    (old_width, old_height) = img.size
    return float(old_height) / float(old_width)


def get_resized_width(img: ImgFilepath, width: int = 480) -> Image:
    f"""
    Resize an image to a desired width, maintaining it's aspect ratio
    {IMG_PARAM}
    {WIDTH_PARAM}
    """
    img = from_filepath(img)
    aspect_ratio = get_aspect_ratio(img)
    new_dim = (int(aspect_ratio * width), width)
    new_img = image.resize(new_dim)
    return new_img


def get_resized_height(img: ImgFilepath, height: int = 480) -> Image:
    f"""
    Resize an image to a desired width, maintaining it's aspect ratio
    {IMG_PARAM}
    {HEIGHT_PARAM}
    """
    img = from_filepath(img)
    aspect_ratio = get_aspect_ratio(img)
    new_dim = (height, int(aspect_ratio * height))
    new_img = image.resize(new_dim)
    return new_img


def to_grayscale(img: ImgFilepath):
    f"""
    Convert an image to grayscale
    {IMG_PARAM}
    :return Image
    """
    return from_filepath(img).convert("L")


def to_base64(img: ImgFilepath, format: str = "PNG") -> bytes:
    f"""
    Convert an image to base 64 bytestring
    {IMG_PARAM}
    {FORMAT_PARAM}
    :return bytes
    """
    img = from_filepath(img)
    buffered = io.BytesIO()
    img.save(buffered, format=format.upper())
    return base64.b64encode(buffered.getvalue())


def to_filepath(
    img: ImgFilepath, filepath: Optional[str] = None, format: str = "png"
) -> str:
    f"""
    Write an image to filepath
    {IMG_PARAM}
    {OUT_FILEPATH_PARAM}
    {FORMAT_PARAM}
    :return str
    """
    img = from_filepath(img)
    if not filepath:
        filepath = path.make_tempfile(ext=format.lower())
    img.save(filepath, format=format.upper())
    return filepath


def to_thumbnail(img: ImgFilepath, size: int = 640) -> Image:
    f"""
    Create a thumbnail of an image
    {IMG_PARAM}
    {THUMB_SIZE_PARAM}
    :return str
    """
    img = from_filepath(img)
    img.thumbnail(size)
    return img


def to_thumbnail_base64(
    img: ImgFilepath, size: int = 640, format: str = "png"
) -> bytes:
    f"""
    Create a base-64 thumbnail of an image
    {IMG_PARAM}
    {THUMB_SIZE_PARAM}
    {FORMAT_PARAM}
    :return str
    """
    img = from_filepath(img)
    img = to_thumbnail(img, size)
    return to_base64(img, format=format)


def to_thumbnail_filepath(
    img: ImgFilepath,
    size: int = 640,
    filepath: Optional[str] = None,
    format: str = "png",
) -> str:
    f"""
    Create a thumbnail of an image amd write to a file
    {IMG_PARAM}
    {THUMB_SIZE_PARAM}
    {OUT_FILEPATH_PARAM}
    {FORMAT_PARAM}
    :return str
    """
    img = to_thumbnail(img, size, format)
    return to_filepath(img, filepath)


# /////÷///////////
# Identicon generators
# //////////////////


def get_identicon_pixels(
    data: str,
    format: str = "png",
    salt: str = "",
    background: ImgColor = "#f0f0f0",
    block_visibility: int = 140,
    block_size: int = 30,
    border: int = 25,
    size: int = 5,
    hash_func: Optional[Callable] = None,
) -> Image:
    """
    Generating GitHub-like symmetrical identicons.
    End image size = size * block_size + border * 2
    :param data: string
    :param format: output format (JPEG, PNG)
    :param block_size: size for one box (in pixels)
    :param border: size for border (in pixels)
    :param background: color for background. Format "#F4F4F4" or (244, 244, 244)
    :param salt: salt for a more varied result (only string)
    :param block_visibility: block transparency (in hex format. 255 - not transparent)
    :param size: number of blocks used
    :param hash_func: function to create a hash (hashlib.sha1, hashlib.sha256, hashlib.md5, etc)
    :return Image
    """

    if not hash_func:
        if size < 11:
            hash_func = hashlib.sha1
        else:
            hash_func = hashlib.sha512

    hashed = hash_func((str(data) + salt).encode("utf8")).hexdigest()
    color = "#" + hashed[:6] + hex(block_visibility)[2:]

    offset = size % 2
    center = size // 2 + offset
    magic_int_all = 2 ** (size * center)
    magic_int = 2 ** size
    img_size = block_size * size + border * 2

    hash_data = hashed[6 : center * 8]

    if len(hash_data) < center * 8 - 6:
        raise ValueError(
            "Not enough hash size to generate. Please use another hash function or change size."
        )

    p = int(hash_data, 16) % magic_int_all
    img = Image.new("RGB", (img_size, img_size), color=background)
    draw = ImageDraw.Draw(img, "RGBA")

    to = range(center)
    for pos in to:
        data = bin((p >> (size * pos)) % magic_int)[2:].zfill(size)
        for index, visible in enumerate(data):
            if int(visible):
                x0 = block_size * pos + border
                y0 = block_size * index + border
                x1 = x0 + block_size - 1
                y1 = y0 + block_size - 1
                draw.rectangle([x0, y0, x1, y1], fill=color)

                if offset and (pos != to[-1]) or not offset:
                    x0 = block_size * ((size - 1) - pos) + border
                    x1 = x0 + block_size - 1
                    draw.rectangle([x0, y0, x1, y1], fill=color)
    return img


def get_identicon_blocks(
    data: str,
    format: str = "png",
    salt: str = "",
    background: ImgColor = "#f0f0f0",
    block_visibility: int = 140,
    block_size: int = 30,
    border: int = 25,
    size: int = 3,
    hash_func: Optional[Callable] = None,
) -> Image:
    """
    Generating blocks of different colors.
    End image size = size * block_size + border * 2
    :param data: string
    :param format: output format (JPEG, PNG)
    :param block_size: size for one box (in pixels)
    :param border: size for border (in pixels)
    :param background: color for background. Format "#F4F4F4" or (244, 244, 244)
    :param salt: salt for a more varied result (only string)
    :param block_visibility: block
     (in hex format. 255 - not transparent)
    :param size: number of blocks used
    :param hash_func: function to create a hash (hashlib.sha1, hashlib.sha256, hashlib.md5, etc)
    :return Image
    """

    if not hash_func:
        if size == 2:
            hash_func = hashlib.sha1
        elif size == 3:
            hash_func = hashlib.sha256
        else:
            hash_func = hashlib.sha512

    hashed = hash_func((str(data) + salt).encode("utf8")).hexdigest()
    block_visibility = hex(block_visibility)[2:]

    img_size = size * block_size + border * 2
    img = Image.new("RGB", (img_size, img_size), color=background)
    draw = ImageDraw.Draw(img, "RGBA")

    offset = 0
    for x in range(size):
        for y in range(size):
            color = hashed[offset : offset + 6] + block_visibility

            if len(color) != 8:
                raise ValueError(
                    "Not enough hash size to generate. Please use another hash function or change size."
                )

            offset += 6

            x0 = x * block_size + border
            y0 = y * block_size + border
            x1 = x * block_size + block_size - 1 + border
            y1 = y * block_size + block_size - 1 + border
            draw.rectangle([x0, y0, x1, y1], fill="#" + color)

    return img


def get_identicon_layers(
    data: str,
    format: str = "png",
    salt: str = "",
    background: ImgColor = "#f0f0f0",
    block_visibility: int = 140,
    block_size: int = 30,
    border: int = 25,
    size: int = 3,
    hash_func: Optional[Callable] = None,
) -> Image:
    """
    Generation of blocks of different colors located on each other.
    End image size = size * block_size + border * 2
    :param data: string
    :param format: output format (jpeg, png)
    :param block_size: size for one box (in pixels)
    :param border: size for border (in pixels)
    :param background: color for background. Format "#F4F4F4" or (244, 244, 244)
    :param salt: salt for a more varied result (only string)
    :param block_visibility: block transparency (in hex format. 255 - not transparent)
    :param size: number of blocks used
    :param hash_func: function to create a hash (hashlib.sha1, hashlib.sha256, hashlib.md5, etc)
    :return bytes
    """

    if not hash_func:
        if size == 2:
            hash_func = hashlib.sha1
        elif size == 3:
            hash_func = hashlib.sha256
        else:
            hash_func = hashlib.sha512

    hashed = hash_func((str(data) + salt).encode("utf8")).hexdigest()
    block_visibility = hex(block_visibility)[2:]

    img_size = size * block_size + border * 2
    img = Image.new("RGB", (img_size, img_size), color=background)
    draw = ImageDraw.Draw(img, "RGBA")
    block_size = block_size // 2

    offset = 0
    for x in range(size):
        color = hashed[offset : offset + 6] + block_visibility

        if len(color) != 8:
            raise ValueError(
                "Not enough hash size to generate. Please use another hash function or change size."
            )

        offset += 6

        x0 = x * block_size + border
        y0 = x * block_size + border
        x1 = img_size - 1 - x * block_size - border
        y1 = img_size - 1 - x * block_size - border
        draw.rectangle([x0, y0, x1, y1], fill=background)
        draw.rectangle([x0, y0, x1, y1], fill="#" + color)

    return img


# lookup of Identicon Functions
IDENTICON_FUNCS = {
    "pixels": get_identicon_pixels,
    "blocks": get_identicon_blocks,
    "layers": get_identicon_layers,
}
IDENTICON_METHOD_NAMES = list(IDENTICON_FUNCS.keys())


def get_identicon(data: object, method: str = "random", **kwargs: dict) -> Image:
    """
    Create an identicon
    :param data: The data to hash
    :param method: The image-generation method (either ``pixels``, ``block``, or ``layers``, ``random``)
    :return PIL.Image
    """
    if method not in IDENTICON_METHOD_NAMES:
        raise ValueError(f"Identicon generation method '{method}' does not exist")
    if method == "random":
        method = random.choice(IDENTICON_METHOD_NAMES)
    return IDENTICON_FUNCS[method](data, **kwargs)


#####################################
# Image Color Palettes via colorthief
#####################################


def get_color_palette(img: ImgFilepath, **kwargs: dict) -> List[str]:
    f"""
    Get an image's color palette via ``colorthief``
    {IMG_PARAM}
    :return list
    """

    # write to tempfile
    is_temp = False
    if isinstance(img, Image):
        img = to_filepath(img)
        is_temp = True

    # generate palette and cleanup
    color_thief = ColorThief(img)
    hexcodes = color_thief.get_palette(**kwargs)
    if is_temp:
        path.remove(img)
    return palette


def get_primary_color(img: ImgFilepath, **kwargs) -> str:
    f"""
    Get an image's primary color via ``colorthief``
    {IMG_PARAM}
    :return str
    """
    from colorthief import ColorThief

    # write to tempfile
    is_temp = False
    if isinstance(img, Image):
        img = to_filepath(img)
        is_temp = True

    color_thief = ColorThief(img)
    hexcode = color_thief.get_color(**kwargs)
    if is_temp:
        path.remove(img)
    return hexcode


###################################
# Image to Ascii
# (Adapted from: https://raw.githubusercontent.com/RameshAditya/asciify/master/asciify.py)
###################################


ASCII_CHARS = [
    ".",
    ",",
    ":",
    ";",
    "+",
    "*",
    "?",
    "%",
    "S",
    "#",
    "@",
    "&",
    "<",
    ">",
    "=",
]
ASCII_CHARS = ASCII_CHARS[::-1]

BUCKET_PARAM = ":param buckets: The number of buckets for pixel-similarity comparision"
CHARS_PARAM = ":param buckets: The number of buckets for pixel-similarity comparision"


def to_ascii_chars(img: ImgFilepath, buckets=25, chars: List[str] = ASCII_CHARS) -> str:
    f"""
    Convert an image to ascii characters by looking for pixel intesity
    {IMG_PARAM}
    {BUCKET_PARAM}
    {CHARS_PARAM}
    :return str
    """
    img = from_filepath(img)
    initial_pixels = list(img.getdata())
    new_pixels = [chars[pixel_value // buckets] for pixel_value in initial_pixels]
    return "".join(new_pixels)


def to_ascii_art(
    img: ImgFilepath, buckets=25, chars: List[str] = ASCII_CHARS, width: int = 240
) -> str:
    f"""
    Convert an image to ascii art by resizing, converting to grayscale,
    and comparing pixel intensities against a list of ascii characters.
    {IMG_PARAM}
    {BUCKET_PARAM}
    {CHARS_PARAM}
    {WIDTH_PARAM}
    :return str
    """
    img = from_filepath(img)
    img = get_resized_width(img, width=width)
    img = to_grayscale(img)
    pixels = to_ascii_chars(img, buckets, chars)
    len_pixels = len(pixels)

    # Construct the image from the character list
    return "\n".join(
        [pixels[index : index + new_width] for index in range(0, len_pixels, new_width)]
    )
