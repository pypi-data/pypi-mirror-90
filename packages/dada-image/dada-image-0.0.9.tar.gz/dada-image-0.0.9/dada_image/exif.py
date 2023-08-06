"""
Image exif metadata extraction.
"""

# ///////////////////
# Imports
# ///////////////////
import logging
from typing import Optional, Dict, Any

from PIL import Image, ExifTags

from dada_utils import path, dates, etc

from dada_image import utils

# ///////////////////
# Logger
# ///////////////////

EXIF_LOGGER = logging.getLogger()


class ExifError(ValueError):
    pass


# ///////////////////
# Functions
# ///////////////////


def get_exif_fields_from_file(
    filepath: utils.ImgFilepath,
    prefix: str = "exif",
    defaults: dict = {},
    ignore_bytes: bool = True,  # TODO
    **kwargs: dict,
) -> Dict[str, Any]:
    """
    Get exif fields from an image.
    :param filepath: a PIL image or an image filepath
    :param prefix: the prefix to prepend to every field name
    :param defautls: the defaults to overwrite with parsed fields.
    :ignore_bytes: whether or not ot include fields with byte-data in the resulls
    :return dict
    """
    pil_img = utils.from_filepath(filepath)

    raw_data = pil_img._getexif()
    if not raw_data:
        EXIF_LOGGER.debug(f"Could not extract exif data from: {filepath}")
        return {}

    # parse the exif data
    fields = {}
    for raw_key, tag_data in raw_data.items():
        if raw_key in ExifTags.TAGS:
            raw_tag = ExifTags.TAGS[raw_key]

        elif raw_key in ExifTags.GPSTAGS:
            raw_tag = ExifTags.GPSTAGS.get(raw_key, None)

        else:
            continue

        clean_tag = (
            f"{prefix}_{path.camel_to_snake(raw_tag)}".replace(
                f"{prefix}_exif_", f"{prefix}_"
            )
            .replace("_make", "_camera_make")
            .replace("_model", "_camera_model")
        )

        if isinstance(tag_data, bytes) and ignore_bytes:
            EXIF_LOGGER.debug(f"CANNOT PROCESS {clean_tag}")
            continue  # TODO: figure out how to fix this
            # data[clean_tag] = tag_data.decode()
        else:
            if "date_time" in clean_tag:
                fields[clean_tag] = dates.parse(tfields).isoformat()
            else:
                fields[clean_tag] = tag_data

    # prefix keys and return non-null data
    return etc.get_fields_data(fields, prefix, defaults)
