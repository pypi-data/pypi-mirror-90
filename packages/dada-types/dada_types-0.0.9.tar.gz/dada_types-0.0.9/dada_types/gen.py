"""
Library for generating random/fake data
"""
# ///////////////////
# Imports
# ///////////////////

import io
import csv
import json
import yaml
import uuid
import random
import hashlib
import logging
import datetime
from functools import partial
from typing import Union, List, Any, Callable, Tuple, Optional, Dict

from faker import Faker

import dada_settings
from dada_utils import dates
import dada_serde
from dada_text import emoticon


# ///////////////////
# Logger
# ///////////////////

GEN_LOGGER = logging.getLogger()

# ///////////////////
# Reusable Doc Strings
# ///////////////////
MIN_PARAM = ":param min: The lower range to generate within"
MAX_PARAM = ":param max: The upper range to generate within"
BY_PARAM = ":param by: The unit of the range to select from"
DIV_BY_PARAM = ":param div_by: The factor to divide the range by."
SIZE_PARAM = ":param size: The number of characters/bytes to generate"
MIN_LEN_PARAM = (
    ":param min_len: The minimum length (in characters / elements) to generate"
)
MAX_LEN_PARAM = (
    ":param max_len: The maximum length (in characters / elements) to generate"
)
THING_NAME_PARAM = ":param thing_name: The name of the thing to generate (eg: ``num``)"
EXCL_PARAM = ":param excl: A list of thing_names to exclude (eg: ``['num', 'int']``"
N_KEYS_PARAM = ":param n_keys: The number of dictionary keys to generate"
INCL_ARRAYS_PARAM = (
    ":param incl_arrays: Whether or not to include arrays in the generated dictionary"
)
MIN_MAX_PARAM = MIN_PARAM + "\n" + MAX_PARAM
MIN_MAX_BY_PARAM = MIN_MAX_PARAM + "\n" + BY_PARAM
MIN_MAX_BY_DIV_BY_PARAM = MIN_MAX_BY_PARAM + "\n" + DIV_BY_PARAM
MIN_LEN_MAX_LEN_PARAM = MIN_LEN_PARAM + "\n" + MAX_LEN_PARAM
DICT_PARAM = N_KEYS_PARAM + "\n" + INCL_ARRAYS_PARAM + "\n" + EXCL_PARAM

# ///////////////////
# Functions
# ///////////////////

# initialize faker

fake = Faker()

# general purpose generators


def choose(lst: List[Any]) -> Any:
    """
    Choose a random element from a list.
    :param lst: A list of elements
    """
    return random.choice(lst)


def dice() -> bool:
    """
    Simple random switch
    """
    return choose([True, False])


# ///////////////////
# SIMPLE THINGS
# ///////////////////


def random_bool(**kwargs) -> bool:
    """
    Generate a random true/false value.
    """
    return dice()


def random_int(min: int = 0, max: int = 500, by: int = 1, **kwargs):
    f"""
    Generate a random integer
    {MIN_MAX_BY_PARAM}
    """
    return int(choose(range(min, max, by)))


def random_bin(size=50, **kwargs) -> bytes:
    f"""
    Generate a random bytearray
    {SIZE_PARAM}
    """
    return bytearray(random.getrandbits(8) for _ in range(size))


def random_num(
    min: int = -10000, max: int = 10000, by: int = 1, div_by: int = 100, **kwargs
) -> float:
    f"""
    Generate a random number, optionally scaling it up and down by a factor of ``div_by``
    {MIN_MAX_BY_DIV_BY_PARAM}
    """
    return (choose(range(min * div_by, max * div_by, by)) * 1.0) / (div_by * 1.0)


def random_per(div_by: int = 100, **kwargs) -> float:
    f"""
    Generate a random percentage, optionally scaling it up and down by a factor of ``div_by``
    {MIN_MAX_BY_DIV_BY_PARAM}
    """
    return random_num(0, 100, 5, div_by, **kwargs)


def random_date(
    base: datetime.datetime = dates.before(days=10000),
    dir: str = "asc",
    unit: str = "days",
    num: int = 10000,
    **kwargs,
) -> str:
    """
    Generate a random date.
    :param base: The base date to generate a range to select from.
    :param dir: The direction to generate the range (either `asc` or `desc`)  to select from.
    :param unit: The unit of the range (`days`, `weeks`, etc..)  to select from.
    :param num: The size of the range to select from.
    :return str
    """
    return choose(dates.date_range(base, dir, unit, num))


def random_time(**kwargs,) -> str:
    """
    Generate a random date.
    :param base: The base date to generate a range to select from.
    :param dir: The direction to generate the range (either `asc` or `desc`)  to select from.
    :param unit: The unit of the range (`days`, `weeks`, etc..)  to select from.
    :param num: The size of the range to select from.
    :return str
    """
    return random_date(**kwargs).time()


def random_emoji(**kwargs) -> str:
    """
    Generate a random emoji.
    """
    return emoticon.emoji_gen_random()


# faker-based generators


def random_hex_code(hue: str = "pink", luminosity: str = "random", **kwargs) -> str:
    """
    Generate a random color
    :param hue:  one of ``monochrome``, ``red``, ``orange``, ``yellow``, ``green``, ``blue``, ``purple``, and ``pink``.
    :param luminosity: either 'bright', 'dark', 'light', or 'random'.
    """
    return fake.color(hue, luminosity, **kwargs)


def random_coordinate(**kwargs) -> float:
    """
    Generate a random lat/long coordinate
    """
    return fake.coordinate()


def random_coordinates(**kwargs) -> List[float]:
    """
    Generate a pair of lat/long coordinates.
    """
    return [random_coordinate(**kwargs), random_coordinate(**kwargs)]


def random_name(**kwargs) -> str:
    """
    Generate a random name (eg first name)
    """
    return fake.name()


def random_slug(**kwargs) -> str:
    """
    Generate a random name
    """
    return fake.slug()


def random_snake(**kwargs) -> str:
    """
    Generate a random snake_case string
    """
    return random_slug(**kwargs).replace("-", "_")


def random_mimetype(**kwargs) -> str:
    """
    Generate a random mimetype
    """
    return fake.mime_type()


def random_file_name(**kwargs) -> str:
    """
    Generate a random file name
    """
    return fake.file_name()


def random_file_path(**kwargs) -> str:
    """
    Generate a random file name
    """
    return "/tmp/" + fake.file_name()


def random_file_ext(**kwargs) -> str:
    """
    Generate a random file extension (without a ``.``)
    """
    ext = fake.file_extension()
    ext.replace(".", "")
    return ext


def random_cron(**kwargs) -> str:
    """
    Generate a random cronstring
    """
    return f"{random_int(0, 60)} {random_int(0, 23)} * * *"


def random_email(**kwargs) -> str:
    """
    Generate a random email
    """
    return fake.email()


def random_user_name(**kwargs) -> str:
    """
    Generate a random name
    """
    return fake.user_name()


def random_url(**kwargs) -> str:
    """
    Generate a random url
    """
    return fake.url()


def random_s3_url(**kwargs) -> str:
    """
    Generate a random s3 url
    :return str
    """
    return fake.url(schemes="s3")


def random_language(**kwargs) -> str:
    """
    Generate a random name
    :return str
    """
    return fake.language_code()


# dada-lake-specific generators


def random_year(
    min: int = 1950, max: int = int(dates.now().year), by: int = 1, **kwargs
) -> int:
    f"""
    Generate a random four-digit year
    {MIN_MAX_BY_PARAM}
    :return int
    """
    return random_int(min, max, by)


def random_duration(
    min: int = 0, max: int = 300, by: int = 1, div_by: int = 100, **kwargs
) -> float:
    f"""
    Generate a random audio/video duration time.
    {MIN_MAX_BY_DIV_BY_PARAM}
    :return float
    """
    return random_num(min, max, by, div_by)


def random_byte_size(min: int = 0, max: int = 16000, by: int = 1, **kwargs) -> int:
    f"""
    Generate a random number reprensenting a file size in bytes.
    {MIN_MAX_BY_PARAM}
    :return int
    """
    return random_int(min, max, by)


def random_bit_rate(min: int = 96, max: int = 48000, by: int = 1024, **kwargs) -> int:
    f"""
    Generate a random integer reprensenting a file bit rate
    {MIN_MAX_BY_PARAM}
    """
    return random_int(min, max, by)


def random_sample_rate(min: int = 1024, max: int = 96000, by: int = 1, **kwargs) -> int:
    f"""
    Generate a random integer reprensenting a file sample rate
    {MIN_MAX_BY_PARAM}
    """
    return random_int(min, max, by)


def random_check_sum(**kwargs) -> str:
    f"""
    Generate a random md5 hash
    """
    return hashlib.md5(str(uuid.uuid4()).encode("utf-8")).hexdigest()


def random_short_hash(max_len=9, **kwargs):
    f"""
    Generate a shortened md5 hash
    {MAX_LEN_PARAM}
    """
    return random_check_sum()[0:max_len].strip()


def random_text(min_len: int = 5, max_len: int = 80, **kwargs) -> str:
    f"""
    Generate a random text string
    {MIN_LEN_MAX_LEN_PARAM}
    """
    start_index = choose(
        range(max_len, dada_settings.FIELD_DEFAULTS_RANDOM_TEXT_LENGTH - max_len, 1)
    )
    text = dada_settings.FIELD_DEFAULTS_RANDOM_TEXT[
        start_index : start_index + max_len
    ].strip()
    text_length = random_int(min=min_len, max=max_len)
    return text[0:text_length]


def random_genre(**kwargs) -> str:
    """
    Generate a random musical genre
    """
    return (
        choose(dada_settings.FIELD_DEFAULTS_RANDOM_GENRE_WORD_1)
        + " "
        + choose(dada_settings.FIELD_DEFAULTS_RANDOM_GENRE_WORD_2)
    )


def random_codec(**kwargs) -> str:
    """
    generate a random audio codec
    (one of: ``H.265``, ``H.264``, ``MP4``, ``MP3`` for now)
    """
    return choose(["H.265", "H.264", "MP4", "MP3"])


def random_musical_key(**kwargs) -> str:
    """
    Generate a random musical genre (eg. ``Am``)
    """
    return choose(dada_settings.AUDIO_DEFAULTS_VALID_KEYS)


def random_harmonic_code(**kwargs) -> str:
    """
    Generate a harmonic code (eg: ``1A``)
    """
    return choose(dada_settings.AUDIO_DEFAULTS_VALID_HARMONIC_CODES)


def random_bpm(**kwargs) -> float:
    """
    Generate a random bpm (eg: ``120.0``)
    """
    return random_num(
        min=dada_settings.AUDIO_DEFAULTS_VALID_BPM_MIN,
        max=dada_settings.AUDIO_DEFAULTS_VALID_BPM_MIN,
        by=1,
        div_by=10 ^ dada_settings.AUDIO_DEFAULTS_BPM_DECIMALS,
    )


def random_track_num(**kwargs) -> int:
    """
    Generate a random track number (eg: ``10``)
    """
    return random_int(1, 16, 1)


def random_disc_num(**kwargs) -> int:
    """
    Generate a random disc number (eg: ``2``)
    """
    return random_int(1, 4, 1)


def random_album_name(**kwargs) -> str:
    """
    Generate a randon album name (eg ``The sound of fury EP``)
    """
    return (
        choose(dada_settings.FIELD_DEFAULTS_RANDOM_ALBUM_NAME_WORD_1)
        + " "
        + choose(dada_settings.FIELD_DEFAULTS_RANDOM_ALBUM_NAME_WORD_2)
        + " "
        + choose(dada_settings.FIELD_DEFAULTS_RANDOM_ALBUM_NAME_WORD_3)
        + " "
        + choose(dada_settings.FIELD_DEFAULTS_RANDOM_ALBUM_NAME_WORD_4)
        + ", "
        + choose(dada_settings.FIELD_DEFAULTS_RANDOM_ALBUM_NAME_WORD_5)
    )


def random_artist_name(**kwargs) -> str:
    """
    Generate a random artist name (eg. ``DJ Steve``)
    """
    return (
        choose(dada_settings.FIELD_DEFAULTS_RANDOM_ARTIST_NAME_WORD_1)
        + " "
        + random_name()
    ).strip()


def random_folder_name(**kwargs) -> str:
    """
    Generate a random folder name (eg: ``downtempo_chillers``)
    """
    return (
        random_genre()
        + "_"
        + choose(dada_settings.FOLDER_DEFAULTS_RANDOM_FOLDER_NAME_WORD_2)
    ).lower()


def random_desktop_name(**kwargs) -> str:
    """
    Generate a random desktop name (eg: ``dev_space``)
    """
    return (
        choose(dada_settings.DESKTOP_DEFAULTS_RANDOM_DESKTOP_NAME_WORD_1)
        + "_"
        + choose(dada_settings.DESKTOP_DEFAULTS_RANDOM_DESKTOP_NAME_WORD_2)
    ).lower()


def random_field_name(**kwargs) -> str:
    """
    Generate a random field name (eg: ``foo_bar``)
    """
    return random_snake()


def random_type(**kwargs) -> str:
    """
    Generate a value type
    """
    return choose(
        ["text", "int", "num", "bool", "bin", "json", "array", "int_array", "num_array"]
    )


def random_entity_type(**kwargs) -> str:
    """
    Generate a random entity type (eg: ``file``)
    """
    return choose(["file", "folder", "user", "desktop"])


def random_file_type(**kwargs) -> str:
    """
    Generate a random dada-lake file type (eg: ``audio``)
    """
    return choose(dada_settings.FILE_DEFAULTS_FILE_TYPES)


def random_file_subtype(**kwargs) -> str:
    """
    Generate a random dada-lake file subtype (eg: ``hit``)
    """
    return choose(dada_settings.FILE_DEFAULTS_FILE_SUBTYPES)


# a lookup of generators
# TODO: deprecate for dictionary

SIMPLE_THING_GENERATORS = {
    "folder_name": random_folder_name,
    "audio_codec_name": random_codec,
    "harmonic_code": random_harmonic_code,
    "musical_key": random_musical_key,
    "file_type": random_file_type,
    "file_subtype": random_file_subtype,
    "desktop_name": random_desktop_name,
    "field_name": random_field_name,
    "artist": random_artist_name,
    "album_artist": random_artist_name,
    "artist_name": random_artist_name,
    "album": random_album_name,
    "album_name": random_album_name,
    "album_title": random_album_name,
    "genre": random_genre,
    "bytes": random_bin,
    "duration": random_duration,
    "date": random_date,
    "type": random_type,
    "created_at": random_date,
    "updated_at": random_date,
    "deleted_at": random_date,
    "name": random_name,
    "user_name": random_user_name,
    "email": random_email,
    "url": random_url,
    "s3": random_s3_url,
    "s3_url": random_s3_url,
    "s3url": random_s3_url,
    "ext": random_file_ext,
    "file_ext": random_file_ext,
    "year": random_year,
    "snake": random_snake,
    "slug": random_slug,
    "language": random_language,
    "mimetype": random_mimetype,
    "entity_type": random_entity_type,
    "lat": random_coordinate,
    "long": random_coordinate,
    "latitude": random_coordinate,
    "longitude": random_coordinate,
    "coordinates": random_coordinates,
    "codec": random_codec,
    "hex_code": random_hex_code,
    "hexcode": random_hex_code,
    "track_title": partial(random_text, min_len=10, max_len=50),
    "track_num": random_track_num,
    "sample_rate": random_track_num,
    "bit_rate": random_bit_rate,
    "sample_rate": random_sample_rate,
    "disc_num": random_disc_num,
    "disc_total": random_track_num,
    "filename": random_file_name,
    "file_name": random_file_name,
    "filename": random_file_name,
    "file_name": random_file_name,
    "int": random_int,
    "smallint": random_int,
    "bigint": random_int,
    "num": random_num,
    "per": partial(random_num, min=0, max=100),
    "float": random_num,
    "decimal": random_num,
    "text": partial(random_text, min_len=10, max_len=50),
    "comment": partial(random_text, min_len=10, max_len=140),
    "emoji": random_emoji,
    "bpm": random_bpm,
    "bool": random_bool,
    "byte_size": random_byte_size,
    "check_sum": random_check_sum,
    "short_hash": random_short_hash,
    # "wkt": partial(random_text, min_len=10, max_len=140), # TODO
    # "wkb": partial(random_text, min_len=10, max_len=140), # TODO
}

SIMPLE_THING_NAMES = list(SIMPLE_THING_GENERATORS.keys())


def random_simple_thing(thing_name: str, **kwargs) -> Any:
    f"""
    Generate a random thing given a ``thing_name``
    {THING_NAME_PARAM}
    :return Any
    """
    return SIMPLE_THING_GENERATORS.get(thing_name)(**kwargs)


def any_simple_thing(excl: List[str] = [], **kwargs) -> Any:
    f"""
    Generate a random thing
    {EXCL_PARAM}
    :return Any
    """
    thing_name = choose(list(set(SIMPLE_THING_NAMES) - set(excl)))
    return thing_name, random_simple_thing(thing_name, **kwargs)


# ///////////////////
# ARRAY TYPES
# ///////////////////


def random_array(
    thing_gen: Callable, min_len: int = 1, max_len: int = 20, **kwargs
) -> List[Any]:
    f"""
    Generate a  random array given thing generator ``thing_gen``
    :param thing_gen: a function to generate a random thing
    {MIN_LEN_MAX_LEN_PARAM}
    :return list
    """
    return [
        thing_gen(**kwargs) for _ in range(0, choose(range(min_len, max_len + 1, 1)), 1)
    ]


def random_simple_things(
    thing_name: str, min_len: int = 0, max_len: int = 20, **kwargs
) -> List[Any]:
    f"""
    Generate a  list of random simple thing given a valid ``thing_name``
    {THING_NAME_PARAM}
    {MIN_LEN_MAX_LEN_PARAM}
    :return list
    """
    return random_array(
        SIMPLE_THING_GENERATORS.get(thing_name), min_len, max_len, **kwargs
    )


def any_simple_things(excl: List[str] = [], **kwargs) -> List[Any]:
    f"""
    Generate a list of any simple thing
    {EXCL_PARAM}
    :return list
    """
    thing_name = choose(set(SIMPLE_THING_NAMES) - set(excl))
    return thing_name, random_simple_things(thing_name, **kwargs)


# Array things
ARRAY_THING_GENERATORS = {
    f"{thing_name}_array": partial(random_array, thing_gen=thing_gen)
    for thing_name, thing_gen in SIMPLE_THING_GENERATORS.items()
}

ARRAY_THING_NAMES = list(ARRAY_THING_GENERATORS.keys())

# ///////////////////
# COMPLEX TYPES
# ///////////////////


def random_param_def(n_keys: int = 2, **kwargs) -> Dict[str, Any]:
    f"""
    Generate a random function param definition
    """
    par_def = {}
    for i in range(n_keys):
        k = choose(["boo", "bar", "baz"])
        t = choose(["text", "int", "num", "date"])
        par_def[k] = {"name": k.title(), "type": t, "info": f"{k} parameter"}
    return par_def


def random_param_val(n_keys: int = 2, **kwargs) -> Dict[str, Any]:
    f"""
    Generate a random function param value
    """
    par_val = {}
    for i in range(n_keys):
        k = choose(["boo", "bar", "baz", "uqbar", ""])
        v = random_int()
        par_val[k] = v
    return par_val


def random_dict(
    n_keys: int = 10, incl_arrays: bool = False, excl: List[Any] = [], **kwargs
) -> dict:
    f"""
    Generate a random dictionary
    {DICT_PARAM}
    :return dict
    """
    data = {}
    # avoid recursion
    for _ in range(n_keys):
        if incl_arrays:
            if dice():
                key, value = any_simple_things(excl)
            else:
                key, value = any_simple_thing(excl)
        else:
            key, value = any_simple_thing(excl)
        data[key + "_" + random_snake()] = str(value)
    return data


def random_json(
    n_keys: int = 10, incl_arrays: bool = False, excl: List[str] = [], **kwargs
) -> str:
    f"""
    Generate a random json string
    {DICT_PARAM}
    :return str
    """
    return json.dumps(random_dict(n_keys, incl_arrays, excl))


def random_yaml(
    n_keys: int = 10, incl_arrays: bool = False, excl: List[str] = [], **kwargs
) -> str:
    f"""
    Generate a random yaml string
    {DICT_PARAM}
    :return str
    """
    return yaml.dumps(random_dict(n_keys, incl_arrays, excl))


def random_csv(
    n_rows: int = 10, n_keys: int = 10, excl: List[str] = [], **kwargs
) -> str:
    f"""
    Generate a random csv string
    :param n_rows: The number of rows to generate
    {DICT_PARAM}
    :return str
    """
    data = [random_dict(n_keys, incl_arrays=False, excl=excl) for _ in range(n_rows)]
    fieldnames = list(data[0].keys())
    csvfile = io.BytesIO()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
    return str(csvfile.getvalue())


# Map/Dict things
MAP_THING_GENERATORS = {
    "map": random_dict,
    "dict": random_dict,
    "json": random_json,
    # "yaml": random_yaml,
    # "yml": random_yaml,
    # "csv": random_csv,
}

MAP_THING_NAMES = list(MAP_THING_GENERATORS.keys())


# ///////////////////
# EVERYTHING
# ///////////////////


THING_GENERATORS = dict(
    list(SIMPLE_THING_GENERATORS.items()) + list(ARRAY_THING_GENERATORS.items())
)
THING_NAMES = SIMPLE_THING_NAMES + ARRAY_THING_NAMES + MAP_THING_NAMES


def random_thing(
    type: Optional[str] = None,
    name: Optional[str] = None,
    infer_thing: bool = False,
    **kwargs,
) -> Any:
    """
    Generate a random thing given its type and name
    :param type: A thing type (eg: `num`)
    :param nam: A thing name (eg `bpm`)
    :param infer_thing: Whether or not to infer thing from the name
    :return Any
    """
    try:
        # First use the literal e for special things
        thing_gen = None
        if name:
            thing_gen = THING_GENERATORS.get(name)

        if not infer_thing:
            if type and not thing_gen:
                thing_gen = THING_GENERATORS.get(type)

        # next sett if the column name has part of a type
        if not thing_gen and name is not None:
            for type in THING_GENERATORS.keys():
                if name in type or type in name:
                    thing_gen = THING_GENERATORS.get(type)
                    if not thing_gen:
                        continue
                    break

        # next just use the optionally provided type
        if type and not thing_gen:
            thing_gen = THING_GENERATORS.get(type)

        # default to text
        if not thing_gen:
            kwargs.setdefault("max_len", 8)
            thing_gen = random_text

        # run generation function
        return thing_gen(**kwargs)

    except Exception as e:
        raise ValueError(
            f"Could not generate {type}: {name} using {thing_gen} because of: {e}"
        )


def anything(excl: List[str] = [], **kwargs) -> Tuple[str, Any]:
    f"""
    Generate anything return the thing_name and generated value
    {EXCL_PARAM}
    :return tuple
    """
    name = choose(set(THING_NAMES) - set(excl))
    return name, random_thing(name, **kwargs)
