"""
Functions for inferring schema from a file.
"""
import urllib.parse
from collections import OrderedDict
from typing import List, Union, Tuple, Any, NewType, Optional

import dada_settings
from dada_types import T
from dada_utils import path, dates

# /////////////
# Custom Types
# /////////////

Filepath = NewType("Filepath", str)  # A filepath string

# ///////////////////
# Reusable Doc Strings
# ///////////////////

PATH_PARAM = ":param path: A filepath as a string"


#
# file metadata
#


def get_dada_type_from_file_metadata(**file_metadata: dict) -> T.dada_type:
    """
    Infer the dada type from file metadata
    """
    ext = file_metadata.get("ext")
    mt = file_metadata.get("mimetype")
    dada_type = None
    if ext is not None:
        dada_type = get_dada_type_from_ext(ext)
    if not dada_type and mt is not None:
        dada_type = get_dada_type_from_mimetype(mt)
    return dada_type


# dada schema extraction
def get_dada_type_from_ext(ext: T.ext.py_optional) -> T.file_type.py_optional:
    """
    Infer the dada type from the file's extension
    """
    if not ext:
        return None
    for dada_type, extensions in dada_settings.FILE_VALID_TYPE_EXT_MIMETYPE.items():
        if ext in list(extensions.keys()):
            return dada_type
    return None


def get_dada_type_from_mimetype(
    mimetype: T.mimetype.py_optional,
) -> T.file_type.py_optional:
    """
    Infer the dada type from the file's mimetype
    """
    if not mimetype:
        return None
    for dada_type, mimetypes in dada_settings.FILE_VALID_TYPE_MIMETYPE_EXT.items():
        if mimetype in list(mimetypes.keys()):
            return dada_type
    return None


def get_default_dada_subtype_for_dada_type(
    type: T.file_type.py,
) -> T.file_subtype.py_optional:
    """
    Get the default dada subtype given a dada type
    """

    return dada_settings.FILE_DEFAULTS_DEFAULT_FILE_SUBTYPE_FOR_FILE_TYPE.get(
        type, dada_settings.FILE_DEFAULTS_DEFAULT_FILE_SUBTYPE
    )


DATE_ATTR = ["year", "month", "day", "hour"]
DATE_FIELDS = ["created_at", "updated_at"]


def get_dada_date_attributes_from_file_metadata(**file_meta) -> dict:
    """
    Extract date parttitions (year, month, day, and hour) from
    """
    data = {}
    for field in DATE_FIELDS:
        val = file_meta.get(field, None)
        if val is None:
            continue
        if isinstance(val, str):
            val = dates.from_string(val)
        for attr in DATE_ATTR:
            name = f"{field.split('_')[0]}_{attr}"
            attr_value = getattr(val, attr)
            if attr_value is not None:
                data[name] = attr_value
                # add year 2
                if name.endswith("_year"):
                    data[name + "2"] = str(attr_value)[2:]
    return data


def get_location(
    path: Filepath,
    internal_s3_bucket_name: str = dada_settings.S3_BUCKET,
    internal_local_dir: str = dada_settings.LOCAL_DIR,
) -> Union[str, None]:
    f"""
    Guess a file's location given it's path (local, s3_int, s3_ext, web)
    {PATH_PARAM}
    :return str
    """
    result = urllib.parse.urlparse(path)

    # definitely an s3 file
    if result.scheme == "s3":
        if result.netloc == internal_s3_bucket_name:
            return "s3_int"
        return "s3_ext"

    # probably a web file
    if result.scheme.startswith("http"):
        return "web"

    if result.scheme == "":
        if (
            ".com" in result.path
            or "www." in result.path
            or ".org" in result.path
            or ".net" in result.path
            or ".io" in result.path
            # ...
        ):
            return "web"

    if result.path.startswith(internal_local_dir):
        return "loc_int"

    elif result.path.startswith("/"):
        return "loc_ext"

    elif result.path is not "":
        return "loc_rel"

    return None
