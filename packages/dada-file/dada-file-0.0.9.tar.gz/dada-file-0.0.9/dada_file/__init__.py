import os
import glob

from dada_utils import path
from dada_file.core import (
    S3ExtFile,
    S3IntFile,
    LocExtFile,
    LocIntFile,
    WebFile,
    DADA_FILE_EXT,
)
from dada_file.schema import get_location
from dada_file.partition import to_glob

import dada_settings

FILE_LOCATIONS = {
    "s3_ext": S3ExtFile,
    "s3_int": S3IntFile,
    "loc_ext": LocExtFile,
    "loc_int": LocIntFile,
    "web": WebFile,
}


def load(url, location=None, **kwargs):
    """
    Load a file into the local store
    """

    # determine location / prepare url
    if not location:
        location = get_location(url)
        if location == "loc_rel":
            url = path.get_full(url)
            location = "loc_ext"
    return FILE_LOCATIONS.get(location)(url, location, **kwargs)


def find_in_local_store(**kwargs):
    """
    List files in the local store given partition a list of partition values
    """
    glob_path = os.path.expanduser(
        path.join(dada_settings.LOCAL_DIR, to_glob(**kwargs))
    )
    for fp in glob.glob(glob_path, recursive=True):
        if not fp.endswith(DADA_FILE_EXT):
            df = load(fp, location="loc_int", **kwargs)
            df.fetch_dada()
            yield df
