"""
A comprehensive dictionary of atomic types for:
    - sqlalchemy
    - python 
    - marshmallow 
    - random generation 
    - serialization / deserialization
    TODO: cut these down there is a max of 255 on enums!
    TODO:
    - athena
    - pandas 
    - cli
    - ui ?
"""
import json
from copy import copy
from functools import partial
from datetime import datetime, time
from typing import Dict, Any, List, Optional, Union, NewType, Tuple

from sqlalchemy.dialects.postgresql import ARRAY, JSONB, ENUM
from sqlalchemy import types
from marshmallow import fields, validate

# TODO: import cli types from click (https://click.palletsprojects.com/en/7.x/parameters/#parameter-types)

import dada_settings
from dada_utils import dates, path
import dada_serde
import dada_text

from dada_types import gen, col, hum

# /////////
# TYPE DICTIONARY
# /////////


# DEFAULT SETTINGS
SMALL_INT_SIZE = 32_767
INT_SIZE = 2_147_483_647
BIG_INT_SIZE = 9_223_372_036_854_775_808
URL_MAX_LENGTH = 1024
EMAIL_MAX_LENGTH = 128
EMOJI_MAX_LENGTH = 4
PATH_MAX_LENGTH = 512
MIMETYPE_MAX_LENGTH = 256
EXT_MAX_LENGTH = 16


def NewVal(type: str, obj: Any) -> Any:
    """
    Internal helper for creating  a new marshmallow value
    with a custom __dada_type__
    """
    new_obj = copy(obj)
    new_obj.__dada_type__ = type
    return new_obj


# TODO: Add better validations error messages for each type via Marshmallow
# TODO: Add stuff like mp3, mov, gltf, here. make each filetype a first class object with built in methods
#       This will make it much easier to write macros

SCALAR_TYPES = {
    # Dada-Lake TYPES
    "dada_type": {
        "info": "A Dada-Lake Type",
        "cat": ["text", "enum"],
        "py": NewType("dada_type", str),
        "col": ENUM,
        "gen": gen.random_type,
        "opts": [],
    },
    "file_type": {
        "info": "File Type",
        "cat": ["text", "enum", "file"],
        "col": ENUM,
        "py": NewType("dada_file_type", str),
        "gen": gen.random_file_type,
        "opts": dada_settings.FILE_DEFAULTS_FILE_TYPES,
    },
    "file_subtype": {
        "info": "File Subtype",
        "cat": ["text", "enum", "file"],
        "col": ENUM,
        "py": NewType("dada_file_subtype", str),
        "gen": gen.random_file_subtype,
        "opts": dada_settings.FILE_DEFAULTS_FILE_SUBTYPES,
    },
    "entity_type": {
        "info": "Entity Type",
        "cat": ["text", "enum"],
        "col": ENUM,
        "py": NewType("dada_entity", str),
        "gen": gen.random_entity_type,
    },
    # TEXT
    "text": {
        "info": "Text",
        "py": NewType("dada_text", str),
        "col": col.TextCol,
        "gen": gen.random_text,
    },
    # NUMERIC
    "smallint": {
        "info": "Small Integer",
        "cat": ["int", "num"],
        "load": int,
        "py": NewType("dada_smallint", int),
        "col": col.SmallIntCol,
        "sql": "SMALLINT",
        "val": fields.Int(
            missing=None,
            validate=validate.Range(min=-SMALL_INT_SIZE, max=SMALL_INT_SIZE),
        ),
        "gen": partial(gen.random_int, min=-SMALL_INT_SIZE, max=SMALL_INT_SIZE),
    },
    "int": {
        "info": "Integer",
        "cat": ["int", "num"],
        "load": int,
        "py": NewType("dada_int", int),
        "col": col.IntCol,
        "sql": "INTEGER",
        "val": fields.Int(
            missing=None, validate=validate.Range(min=-INT_SIZE, max=INT_SIZE)
        ),
        "gen": partial(gen.random_int, min=-INT_SIZE, max=INT_SIZE),
    },
    "bigint": {
        "info": "Big Integer",
        "cat": ["int", "num"],
        "load": int,
        "py": NewType("dada_bigint", int),
        "col": col.BigIntCol,
        "sql": "BIGINT",
        "val": fields.Int(
            missing=None, validate=validate.Range(min=-BIG_INT_SIZE, max=BIG_INT_SIZE)
        ),
        "gen": partial(gen.random_int, min=-BIG_INT_SIZE, max=BIG_INT_SIZE),
    },
    "num": {
        "info": "Number",
        "cat": ["num"],
        "load": float,
        "py": NewType("dada_num", float),
        "col": col.NumCol,
        "sql": "DOUBLE PRECISION",
        "val": fields.Float(missing=None),
        "gen": gen.random_num,
    },
    # IDS
    "id": {
        "info": "Identifier",
        "cat": ["id", "int"],
        "load": int,
        "py": NewType("dada_id", int),
        "col": col.IntCol,
        "sql": "INTEGER",
        "val": fields.Int(missing=None, validate=validate.Range(min=1, max=INT_SIZE)),
        "gen": partial(gen.random_int, min=1, max=INT_SIZE),
        "dump": int,
    },
    "fk": {
        "info": "Foreign Key",
        "cat": ["id", "int"],
        "load": int,
        "py": NewType("dada_fk", int),
        "col": col.IntCol,
        "sql": "INTEGER",
        "val": fields.Int(missing=None, validate=validate.Range(min=1, max=INT_SIZE)),
        "gen": partial(gen.random_int, min=1, max=INT_SIZE),
        "dump": int,
    },
    "pk": {
        "info": "Primary Key",
        "cat": ["id", "int"],
        "load": int,
        "py": NewType("dada_pk", int),
        "col": col.IntCol,
        "sql": "INTEGER",
        "val": fields.Int(missing=None, validate=validate.Range(min=1, max=INT_SIZE)),
        "gen": partial(gen.random_int, min=1, max=INT_SIZE),
        "dump": int,
    },
    "bundle_id": {
        "info": "A File ID representing a collection of other Files",
        "cat": ["id", "int"],
        "load": int,
        "py": NewType("dada_bundle_id", int),
        "col": col.IntCol,
        "sql": "INTEGER",
        "val": fields.Int(missing=None, validate=validate.Range(min=1, max=INT_SIZE)),
        "gen": partial(gen.random_int, min=1, max=INT_SIZE),
        "dump": int,
    },
    # date + time
    "date_tz": {
        "info": "Date (With Timezone)",
        "cat": ["date"],
        "load": dates.from_string,
        "py": NewType("dada_date_tz", datetime),
        "col": col.DateTzCol,
        "sql": "TIMESTAMP WTIH TIMEZONE",
        "val": fields.DateTime(missing=None),
        "gen": dates.now,
        "dump": lambda x: x.isoformat(),
    },
    "created_at": {
        "info": "Entity Creation Date",
        "cat": ["date"],
        "load": dates.from_string,
        "py": NewType("dada_created_at", datetime),
        "col": col.DateTzCol,
        "sql": "TIMESTAMP WTIH TIMEZONE",
        "val": fields.DateTime(missing=None),
        "gen": dates.now,
        "dump": lambda x: x.isoformat(),
    },
    "updated_at": {
        "info": "Entity Updated Date",
        "cat": ["date"],
        "load": dates.from_string,
        "py": NewType("dada_updated_at", datetime),
        "col": col.DateTzCol,
        "sql": "TIMESTAMP WTIH TIMEZONE",
        "val": fields.DateTime(missing=None),
        "gen": dates.now,
        "dump": lambda x: x.isoformat(),
    },
    "deleted_at": {
        "info": "Entity Deleted Date",
        "cat": ["date"],
        "load": dates.from_string,
        "py": NewType("dada_deleted_at", datetime),
        "col": col.DateTzCol,
        "sql": "TIMESTAMP WTIH TIMEZONE",
        "val": fields.DateTime(missing=None),
        "gen": dates.now,
        "dump": lambda x: x.isoformat(),
    },
    "file_modified_at": {
        "info": "Entity file Modified Date",
        "cat": ["date"],
        "load": dates.from_string,
        "py": NewType("dada_file_modified_at", datetime),
        "col": col.DateTzCol,
        "sql": "TIMESTAMP WTIH TIMEZONE",
        "val": fields.DateTime(missing=None),
        "gen": dates.now,
        "dump": lambda x: x.isoformat(),
    },
    "date": {
        "info": "Date",
        "cat": ["date"],
        "load": dates.from_string,
        "py": NewType("dada_date", datetime),
        "col": col.DateCol,
        "sql": "TIMESTAMP",
        "val": fields.DateTime(missing=None),
        "gen": dates.now,
        "dump": lambda x: x.isoformat(),
    },
    "time_tz": {
        "info": "Time (With Timezone)",
        "cat": ["time"],
        "load": lambda x: dates.from_string(x).time(),
        "py": NewType("dada_time_tz", time),
        "col": col.TimeTzCol,
        "sql": "TIME WITH TIMEZONE",
        "val": fields.Time(missing=None),
        "gen": dates.now,
        "dump": lambda x: x.isoformat(),
        "hum": lambda x: x.strftime("%B"),
    },
    "time": {
        "info": "Time",
        "cat": ["time"],
        "load": lambda x: dates.from_string(x).time(),
        "py": NewType("dada_time", datetime),
        "col": col.TimeCol,
        "sql": "TIME",
        "val": fields.Time(missing=None),
        "gen": dates.now,
        "dump": lambda x: x.isoformat(),
    },
    "seconds": {
        "info": "Seconds",
        "cat": ["time"],
        "load": float,
        "py": NewType("dada_seconds", float),
        "col": col.NumCol,
        "sql": "DOUBLE PRECISION",
        "val": fields.Float(missing=None),
        "gen": gen.random_num,
        "dump": str,
    },
    #  ETC
    "bin": {
        "info": "Binary",
        "cat": ["bin"],
        "load": bytes,
        "py": NewType("dada_bin", bytes),
        "col": col.BinCol,
        "sql": "LargeBinary",
        "val": fields.Raw,
        "gen": gen.random_bin,
    },
    "bool": {
        "info": "True/False",
        "cat": ["bool"],
        "load": dada_text.to_bool,
        "py": NewType("dada_bool", bytes),
        "col": col.BoolCol,
        "sql": "BOOLEAN",
        "val": fields.Boolean(missing=None),
        "gen": gen.random_bool,
        "dump": str,
    },
    "enum": {
        "info": "ENUM",
        "cat": ["text", "enum"],
        "py": NewType("dada_enum", str),
        "col": ENUM,
        "gen": gen.random_text,
    },
    # GEO
    # "lat": {
    #     "info": "Latitude",
    #     "cat": ["geo", "num"],
    #     "load": float,
    #     "py": NewType("dada_lat", float),
    #     "col": col.NumCol,
    #     "sql": "DOUBLE PRECISION",
    #     "val": fields.Float(missing=None),
    #     "gen": gen.random_coordinate,
    # },
    # "long": {
    #     "info": "Longitude",
    #     "cat": ["geo", "num"],
    #     "load": float,
    #     "py": NewType("dada_long", float),
    #     "col": col.NumCol,
    #     "sql": "DOUBLE PRECISION",
    #     "val": fields.Float(missing=None),
    #     "gen": gen.random_coordinate,
    # },
    # TODO
    # "wkt": {
    #     "info": "Geometry as Well-known Text",
    #     "cat": ["geo"],
    #     "py": NewType("dada_wkt", float),
    #     "col": col.WKTCol,
    #     "sql": "TEXT",
    #     "val": fields.Float(missing=None),
    #     "gen": gen.random_coordinate,
    # },
    # "wkb": {
    #     "info": "Geometry as Well-known Binary",
    #     "cat": ["geo"],
    #     "py": NewType("dada_wkb", bytes),
    #     "col": col.WKBCol,
    #     "sql": "GEOMETRY",
    #     "val": fields.Float(missing=None),
    #     "gen": gen.random_coordinate,
    # },
    # CUSTOM TEXT
    "name": {
        "info": "Name",
        "py": NewType("dada_name", str),
        "col": col.TextCol,
        "gen": gen.random_text,
    },
    "slug": {
        "info": "Slug",
        "py": NewType("dada_slug", str),
        "col": col.TextCol,
        "gen": gen.random_slug,
    },
    "info": {
        "info": "Info",
        "py": NewType("dada_info", str),
        "col": col.TextCol,
        "gen": gen.random_text,
    },
    # TODO: make this load PIL Image
    "img": {
        "info": "Base-64 encoded Image",
        "cat": ["text", "theme"],
        "py": NewType("dada_img", str),
        "col": col.TextCol,
        "gen": gen.random_text,
    },
    # CUSTOM STRINGS
    "hex_code": {
        "info": "Color as a hexcode",
        "cat": ["text", "theme"],
        "py": NewType("dada_hex_code", str),
        "col": col.TextCol,
        "val": fields.Str(missing=None, validate=validate.Length(max=EMOJI_MAX_LENGTH)),
        "gen": gen.random_emoji,
    },
    "emoji": {
        "info": "Emoji",
        "cat": ["text", "theme"],
        "py": NewType("dada_emoji", str),
        "col": col.TextCol,
        "val": fields.Str(missing=None, validate=validate.Length(max=EMOJI_MAX_LENGTH)),
        "gen": gen.random_emoji,
    },
    "url": {
        "info": "URL",
        "py": NewType("dada_url", str),
        "col": col.TextCol,
        "val": fields.URL(missing=None, validate=validate.Length(max=URL_MAX_LENGTH)),
        "gen": gen.random_url,
    },
    "email": {
        "info": "Email",
        "py": NewType("dada_email", str),
        "col": col.TextCol,
        "val": fields.Email(
            missing=None, validate=validate.Length(max=EMAIL_MAX_LENGTH)
        ),
        "gen": gen.random_email,
    },
    "param_name": {
        "info": "Parameter Name",
        "cat": ["text", "param"],
        "col": col.TextCol,
        "py": NewType("dada_param_name", Dict[str, Any]),
        "val": fields.Dict(missing={}),
        "gen": gen.random_snake,
    },
    # FILE METADATA
    "directory": {
        "info": "File Directory",
        "cat": ["text", "file"],
        "py": NewType("dada_path", str),
        "col": col.TextCol,
        "val": fields.Str(missing=None, validate=validate.Length(max=PATH_MAX_LENGTH)),
        "gen": lambda x: "foo/bar" + gen.random_file_name(),
    },
    "path": {
        "info": "File Path (file_name + ext)",
        "cat": ["text", "file"],
        "py": NewType("dada_path", str),
        "col": col.TextCol,
        "val": fields.Str(missing=None, validate=validate.Length(max=PATH_MAX_LENGTH)),
        "gen": lambda x: "foo/"
        + gen.random_file_name()
        + "."
        + random.random_file_ext(),
    },
    "partition": {
        "info": "File Partition (eg ``date=1914-10-07``)",
        "cat": ["text", "file"],
        "py": NewType("dada_partition", str),
        "col": col.TextCol,
        "gen": lambda x: f"date={dates.now().date().isoformat()}",
    },
    "file_name": {
        "info": "File Name",
        "cat": ["text", "file"],
        "py": NewType("dada_file_name", str),
        "col": col.TextCol,
        "val": fields.Str(missing=None, validate=validate.Length(max=PATH_MAX_LENGTH)),
        "gen": gen.random_file_name,
    },
    "ext": {
        "info": "File Extension",
        "cat": ["text", "file"],
        "py": NewType("dada_ext", str),
        "col": col.TextCol,
        "val": fields.Str(missing=None, validate=validate.Length(max=EXT_MAX_LENGTH)),
        "gen": gen.random_file_ext,
    },
    "mimetype": {
        "info": "File Mimetype",
        "cat": ["text", "file"],
        "py": NewType("dada_mimetype", str),
        "col": col.TextCol,
        "gen": gen.random_mimetype,
    },
    "check_sum": {
        "info": "Checksum Identifier",
        "cat": ["text", "file"],
        "py": NewType("dada_check_sum", str),
        "col": col.TextCol,
        "gen": gen.random_check_sum,
    },
    "byte_size": {
        "info": "File Byte Size",
        "cat": ["int", "file", "num"],
        "load": int,
        "py": NewType("dada_byte_size", int),
        "col": col.IntCol,
        "val": fields.Integer(missing=None),
        "gen": gen.random_byte_size,
        "hum": hum.display_byte_size,
    },
    "position": {
        "info": "Position",
        "cat": ["int"],
        "load": int,
        "py": NewType("dada_position", int),
        "col": col.IntCol,
        "sql": "INTEGER",
        "val": fields.Integer(missing=0, validate=validate.Range(min=0)),
        "gen": gen.random_int,
    },
    "s3_url": {
        "info": "Amazon S3 URL / Digital Ocean",
        "cat": ["text", "file"],
        "py": NewType("dada_s3_url", str),
        "col": col.TextCol,
        "val": fields.URL(
            schemes="s3", missing=None, validate=validate.Length(max=URL_MAX_LENGTH)
        ),
        "gen": gen.random_s3_url,
    },
    "is_private": {
        "info": "Whether or not this resource is visible to other users",
        "cat": ["bool", "file"],
        "load": dada_text.to_bool,
        "py": NewType("dada_is_private", bool),
        "col": col.BoolCol,
        "sql": "BOOLEAN",
        "val": fields.Boolean(missing=True),
        "gen": gen.dice,
    },
    "api_key": {
        "info": "Dada Lake API Key",
        "cat": ["user"],
        "py": NewType("dada_api_key", str),
        "col": col.TextCol,
        "gen": gen.random_short_hash,
        "sensitive": True,
    },
    "password": {
        "info": "Dada Lake Password",
        "cat": ["user"],
        "py": NewType("dada_password", str),
        "col": col.TextCol,
        "gen": gen.random_short_hash,
        "sensitive": True,
    },
    # macro / tasks / job /  querying
    "filter": {
        "info": "Filter String",
        "cat": ["text", "task"],
        "py": NewType("dada_filter", str),
        "col": col.TextCol,
    },
    "sort": {
        "info": "sort String",
        "cat": ["text", "task"],
        "py": NewType("dada_sort", str),
        "col": col.TextCol,
    },
    "api_page": {
        "info": "API Page Number",
        "cat": ["int", "num", "task"],
        "py": NewType("dada_api_page", int),
        "col": col.IntCol,
    },
    "api_per_page": {
        "info": "The Number of Results to return from the api, per page.",
        "cat": ["int", "num", "task"],
        "py": NewType("dada_api_per_page", int),
        "col": col.IntCol,
    },
    "sql": {
        "info": "SQL Query",
        "cat": ["text", "task"],
        "py": NewType("dada_sql", str),
        "col": col.TextCol,
    },
    "search": {
        "info": "Search Query",
        "cat": ["text", "search"],
        "py": NewType("dada_search", str),
        "col": col.TextCol,
    },
    "vector": {
        "info": "Search Vector",
        "cat": ["text", "search"],
        "col": col.SearchVectorCol,
        "py": NewType("dada_vector", str),
        "gen": gen.random_text,
    },
    # JSON
    "json": {
        "info": "JSON",
        "cat": ["json"],
        "load": dada_serde.json_to_obj,
        "col": col.JSONCol,
        "py": NewType("dada_json", Dict[str, Any]),
        "sql": "JSONB",
        "val": fields.Dict(missing={}),
        "gen": gen.random_dict,
        "dump": dada_serde.obj_to_json,
    },
    "param_def": {
        "info": "Parameter Schema Definition",
        "cat": ["json", "param"],
        "load": dada_serde.json_to_obj,
        "col": col.JSONCol,
        "py": NewType("dada_param_def", Dict[str, Any]),
        "sql": "JSONB",
        "val": fields.Dict(missing={}),
        "gen": gen.random_param_def,
        "dump": dada_serde.obj_to_json,
    },
    "param_val": {
        "info": "Parameter Values",
        "cat": ["json", "param"],
        "load": dada_serde.json_to_obj,
        "col": col.JSONCol,
        "py": NewType("dada_param_val", Dict[str, Any]),
        "sql": "JSONB",
        "val": fields.Dict(missing={}),
        "gen": gen.random_param_val,
        "dump": dada_serde.obj_to_json,
    },
    "fields": {
        "info": "Fields",
        "cat": ["json", "fields"],
        "load": dada_serde.json_to_obj,
        "col": col.JSONCol,
        "py": NewType("dada_fields", Dict[str, Any]),
        "sql": "JSONB",
        "val": fields.Dict(missing={}),
        "gen": gen.random_dict,
        "dump": dada_serde.obj_to_json,
    },
}

# text ranges

TEXT_RANGE_INTERVALS = [128, 256, 1024]
TEXT_RANGE_TYPES = {
    f"text_{n}": {
        "info": f"Text (max length: {n})",
        "py": NewType(f"dada_text_{n}", str),
        "col": types.Unicode(length=n),
        "val": fields.Str(missing=None, validate=validate.Length(min=0, max=n)),
        "gen": partial(gen.random_text, max_len=n),
    }
    for n in TEXT_RANGE_INTERVALS
}
TEXT_RANGE_TYPE_NAMES = list(TEXT_RANGE_TYPES.keys())

# entity scalar types
ENTITY_SCALAR_TYPES = {}
for entity in [
    "file",
    "folder",
    "tag",
    "user",
    "field",
    "desktop",
]:  # TODO: parameterize

    ENTITY_SCALAR_TYPES.update(
        {
            f"{entity}_id": {
                "info": f"{entity.title()} Id",
                "cat": [entity, "id", "fk"],
                "load": int,
                "py": NewType(f"dada_{entity}_id", str),
                "col": col.IntCol,
                "sql": "INTGER",
                "val": fields.Int(missing=None, validate=validate.Range(min=1)),
                "gen": partial(gen.random_int, min=0, max=100000),
            },
            f"{entity}_slug": {
                "info": f"{entity.title()} Slug",
                "cat": [entity, "text"],
                "py": NewType(f"dada_{entity}_slug", str),
                "col": col.TextCol,
                "sql": "TEXT",
                "gen": gen.random_slug,
            },
            f"{entity}_id_slug": {
                "info": f"{entity.title()} ID/Slug",
                "cat": [entity, "text", "id"],
                "py": NewType(f"dada_{entity}_id_slug", Union[str, int]),
                "col": col.TextCol,
                "sql": "TEXT",
                "gen": gen.random_slug,
            },
        }
    )

# scalar + text range = simple

SIMPLE_TYPES = dict(
    list(SCALAR_TYPES.items())
    + list(TEXT_RANGE_TYPES.items())
    + list(ENTITY_SCALAR_TYPES.items())
)
SIMPLE_TYPE_NAMES = list(SIMPLE_TYPES.keys())


ARRAY_TYPES_EXCLUDE = [
    "vector",
    "password",
    "api_key",
    "enum",
    "param_def",
    "param_val",
    "json",
    "fields",
    "file_type",
    "file_subtype",
    "entity_type",
    "api_key",
    "api_page",
    "api_per_page",
    "is_private",
    "bin",
]  # we can exclude array types here

ARRAY_TYPES = {
    f"{type}_array": {
        "info": f"Array[ {schema['info']} ]",
        "cat": list(set(["array"] + schema.get("cat", ["text"]))),
        "load": lambda x: [schema.get("load", str)(x) for x in dada_text.to_list(x)],
        "py": NewType(f"{type}", List[schema.get("py", str)]),
        "col": ARRAY(schema.get("col", col.TextCol)),
        "sql": f"{schema.get('sql', 'TEXT')}[]",
        "val": fields.List(schema.get("val", fields.Str(missing=None)), missing=[]),
        "gen": partial(gen.random_array, thing_gen=schema.get("gen", gen.random_text)),
        "dump": dada_serde.obj_to_json,
    }
    for type, schema in SIMPLE_TYPES.items()
    if type not in ARRAY_TYPES_EXCLUDE
}

# special array types
ARRAY_TYPES.update(
    {
        "enum_array": {
            "info": "An array of set values",
            "cat": ["array", "enum"],
            "load": dada_text.to_list,
            "col": col.EnumArrayCol,
            "py": NewType("dada_enum", List[str]),
            "sql": "text[]",
            "val": fields.List(fields.Str, missing=[]),
            "gen": partial(gen.random_simple_things, thing_name="entity_type"),
            "dump": dada_serde.json_to_obj,
        },
        "entity_type_array": {
            "info": "An array of dada entity types",
            "cat": ["array", "enum"],
            "load": dada_text.to_list,
            "col": col.EnumArrayCol,
            "py": NewType("dada_entity_type", List[str]),
            "sql": "text[]",
            "val": fields.List(fields.Str, missing=[]),
            "gen": partial(gen.random_simple_things, thing_name="entity_type"),
            "dump": dada_serde.json_to_obj,
        },
        "file_type_array": {
            "info": "An array of dada file types",
            "cat": ["array", "file", "enum"],
            "load": dada_text.to_list,
            "col": col.EnumArrayCol,
            "py": NewType("dada_file_type", List[str]),
            "sql": "text[]",
            "val": fields.List(fields.Str, missing=[]),
            "gen": partial(gen.random_simple_things, thing_name="file_type"),
            "dump": dada_serde.json_to_obj,
        },
        "file_subtype_array": {
            "info": "An array of dada file subtypes",
            "cat": ["array", "enum", "file"],
            "load": dada_text.to_list,
            "col": col.EnumArrayCol,
            "py": NewType("dada_file_subtype", List[str]),
            "sql": "text[]",
            "val": fields.List(fields.Str, missing=[]),
            "gen": partial(gen.random_simple_things, thing_name="file_subtype"),
            "dump": dada_serde.json_to_obj,
        },
    }
)
ARRAY_TYPE_NAMES = list(ARRAY_TYPES.keys())


# /////////
# ALL TYPES
# /////////


TYPES = dict(list(SIMPLE_TYPES.items()) + list(ARRAY_TYPES.items()))
TYPE_NAMES = list(TYPES.keys())
