# Partitions
#
from datetime import datetime
from collections import OrderedDict

from dada_types import T


PARTITION_SCHEMA = OrderedDict(
    {
        "entity_type": "e",
        "file_type": "t",
        "file_subtype": "s",
        "ext": "x",
        "created_year2": "y",
        "created_month": "m",
        "created_day": "d",
        "created_hour": "h",
        "id": "i",
    }
)
PARTITION_ABRR_TO_ATTR = {v: k for k, v in PARTITION_SCHEMA.items()}

VERSION_KEY = "v"
VERSION_SCHEMA = ["check_sum", "updated_at"]
VERSION_DATE_FORMAT = "%y.%m.%d.%H"


def is_partition_url(url) -> bool:
    """ checks if a url is a dada partitioned url"""
    return all([f"/{k}=" in url for k in PARTITION_ABRR_TO_ATTR.keys()])


def version(**kwargs) -> T.partition.py:
    """ create a version string given kwargs """
    parts = []
    for attr in VERSION_SCHEMA:
        p = kwargs.get(attr, None)
        if not p:
            p = ""
        if isinstance(p, datetime):
            p = p.strftime(VERSION_DATE_FORMAT)
        parts.append(p)
    return f'{VERSION_KEY}={"-".join(parts)}'


def create(**kwargs) -> T.partition.py:
    """ create a partition given kwargs"""
    part_string = ""
    for part, abbr in PARTITION_SCHEMA.items():
        pval = kwargs.get(part, None)
        if pval is None:
            pval = ""
        part_string += f"{abbr}={pval}/"
    return part_string


#
# partiton extraction
#


def extract(url) -> dict:
    """ extract metadata fields from a partitioned url """
    d = {}
    if not is_partition_url(url):
        return d
    to_search = dict(
        list({VERSION_KEY: "version"}.items()) + list(PARTITION_ABRR_TO_ATTR.items())
    )
    for abbr, attr in to_search.items():

        parts = url.split(f"/{abbr}=")
        if len(parts) < 2:
            continue

        if attr != "version":
            value = parts[1].split("/")[0]
            if attr.startswith("created_") or attr == "id":
                if value != "":
                    value = int(value)
                else:
                    value = None
            d[attr] = value

        else:
            version = parts[1].split("/")[0]
            d["version"] = version
            if version != "latest":
                for sub_attr, sub_val in zip(VERSION_SCHEMA, version.split("-")):
                    if sub_attr.endswith("_at"):
                        d[sub_attr] = datetime.strptime(sub_val, VERSION_DATE_FORMAT)

    return extract_dates(d)


def extract_dates(d) -> dict:
    # format dates
    if "created_year2" in d:
        d["created_at"] = datetime(
            **{
                "year": int(f"20{d.get('created_year2', '20')}"),
                "month": int(d.get("created_month", "1")),
                "day": int(d.get("created_day", "1")),
                "hour": int(d.get("created_hour", "0")),
                "minute": int(d.get("created_minute", "0")),
            }
        )

    if "updated_at" in d.keys():
        d["updated_at"] = datetime.strptime(d["updated_at"], VERSION_DATE_FORMAT)
    return d


def to_glob(**kw: dict) -> str:
    """
    Given a dictionary of partially-filled partition fields, constuct a glob pattern to match file paths with.
    """
    # add date partitions
    if "created_at" in kw:
        kw.setdefault("created_year2", kw["created_at"].strftime("%y"))
        kw.setdefault("created_month", kw["created_at"].strftime("%m"))
        kw.setdefault("created_day", kw["created_at"].strftime("%d"))
        kw.setdefault("created_hour", kw["created_at"].strftime("%H"))

    if "updated_at" in kw:
        kw.setdefault("updated_year2", kw["updated_at"].strftime("%y"))
        kw.setdefault("updated_month", kw["updated_at"].strftime("%m"))
        kw.setdefault("updated_day", kw["updated_at"].strftime("%d"))
        kw.setdefault("updated_hour", kw["updated_at"].strftime("%H"))
        kw.setdefault("updated_min", kw["updated_at"].strftime("%M"))

    if not kw.get("latest", False):
        version_string = f"v={kw.get('check_sum', '*')}-{kw.get('updated_year2', '*')}.{kw.get('updated_month', '*')}.{kw.get('updated_day', '*')}.{kw.get('updated_hour', '*')}.{kw.get('updated_min', '*')}/"
    else:
        version_string = "v=latest/"

    return (
        f"e={kw.get('entity_type', '*')}/t={kw.get('file_type', '*')}/s={kw.get('file_subtype', '*')}/"
        + f"x={kw.get('ext', '*')}/y={kw.get('created_year2', '*')}/m={kw.get('created_month', '*')}/"
        + f"d={kw.get('created_day', '*')}/h={kw.get('created_day', '*')}/i={kw.get('id', '*')}/"
        + version_string
        + f"{kw.get('slug', '*')}.{kw.get('ext', '*')}"
    )
