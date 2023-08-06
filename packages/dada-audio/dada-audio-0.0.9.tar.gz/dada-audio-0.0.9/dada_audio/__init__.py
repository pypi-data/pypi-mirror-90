"""
Audio/Music theory utlities
"""

from functools import partial
from typing import Union, Dict, List, Any, NewType

import taglib

import dada_settings
from dada_utils import etc
import dada_text


# ///////////////////
# Custom types
# ///////////////////

RawId3Tag = NewType("RawId3Tag", Union[str, None])


class Id3Error(ValueError):
    pass


# ///////////////////
# Reusable Doc Strings
# ///////////////////

RAW_TAG_PARAM = ":param raw_tag: A raw id3 tag to process"
BPM_PARAM = ":param bpm: The track's bpm (eg: ``120.0``)"
BPM_DECIMALS_PARAM = (
    ":param bpm_decimals: The number of decimals to round the bpm to. (eg: `2`)"
)
DURATION_PARAM = ":param duration: The track's duration  (eg: ``240.0``)"
BPM_DURATION_PARAM = f"{BPM_PARAM}\n{DURATION_PARAM}"

# ///////////////////
# Functions
# ///////////////////


def key_to_harmonic_code(key: str) -> Union[str, None]:
    """
    Get a a harmonic code (eg: ``1A``) from a ``musical_key`` (eg: ``Am``)
    :param key: A musical key (eg: ``Am``)
    :return str
    """
    return dada_settings.AUDIO_DEFAULTS_KEYS_TO_HARMONIC_CODES.get(key, None)


def harmonic_code_to_key(harmonic_code: str) -> Union[str, None]:
    """
    Get a a key (eg: ``Am``) from a ``harmonic_code`` (eg: ``1A``)
    :param harmonic_code: A harmonic code (eg: ``1A``)
    :return str
    """
    return dada_settings.AUDIO_DEFAULTS_HARMONIC_CODES_TO_KEYS.get(harmonic_code, None)


def get_number_of_measures(bpm: float, duration: float) -> int:
    f"""
    Get the number of measures in a song given its bpm / duration
    Formula From: [Music Duration Calculator](https://www.vcalc.com/wiki/Coder/Music+Duration+Calculator)
    ```
    duration = (measures / bpm ) * 60
    measures = ((duration / 60) * bpm ) = measures
    ```
    {BPM_DURATION_PARAM}
    :return int
    """
    return int(round(((duration / 60) * bpm), 0))


def get_number_of_bars(bpm: float, duration: float, bar_length: int = 4) -> float:
    f"""
    Get the esimated number of bars in a track given its bpm and duration and the time signature
    {BPM_DURATION_PARAM}
    :param bar_length: The number of measures in a bar.
    :return float
    """
    return get_number_of_measures(bpm, duration) / float(bar_length)


#  //////////////
# ID3 utilities
# //////////////


def id3_clean_tag_name(raw_tag_name: str) -> str:
    """
    Clean an id3 tag name
    :param raw_tag_name: A raw tag name (eg `ARTIST`)
    :return str
    """
    return raw_tag_name.replace(" ", "").strip().upper()


def id3_clean_tag(raw_tag: RawId3Tag, max_length: int = 512) -> Union[str, None]:
    f"""
    Clean a raw Id3 Tag
    {RAW_TAG_PARAM}
    :return str
    """
    if raw_tag is None or raw_tag.strip() == "":
        return None
    tag = etc.unlist(raw_tag)
    if not tag:
        return None
    tag = dada_text.rm_whitespace(tag)
    if len(tag) > max_length:
        return tag[:max_length]
    return tag


def id3_clean_date(raw_tag: RawId3Tag) -> Union[str, None]:
    f"""
    Clean an id3 date tag
    {RAW_TAG_PARAM}
    :return str
    """
    if raw_tag is None or raw_tag.strip() == "":
        return None
    try:
        return dates.parse(s).isoformat()
    except ValueError:
        return None


def id3_clean_int(raw_tag: RawId3Tag) -> Union[int, None]:
    f"""
    Clean an integer in an id3 tag.
    {RAW_TAG_PARAM}
    :return int
    """
    if raw_tag is None or raw_tag.strip() == "":
        return None
    try:
        return int(s)
    except ValueError:
        pass
    return None


def id3_clean_year(raw_tag: RawId3Tag) -> Union[int, None]:
    f"""
    Clean a year in an id3 tag.
    {RAW_TAG_PARAM}
    :return int
    """
    if raw_tag is None or raw_tag.strip() == "":
        return None
    raw_tag = raw_tag.strip()
    if len(s) == 4:
        try:
            return int(s)
        except ValueError:
            pass
    try:
        return int(dates.parse(s).year)
    except ValueError:
        pass
    return None


def id3_clean_bpm(
    raw_tag: RawId3Tag, bpm_decimals: int = dada_settings.AUDIO_DEFAULTS_BPM_DECIMALS
) -> Union[float, None]:
    f"""
    Clean a bpm in an id3 tag
    {RAW_TAG_PARAM}
    {BPM_DECIMALS_PARAM}
    :return float
    """
    if raw_tag is None or raw_tag.strip() == "":
        return

    # extract all the numbers
    numbers = dada_text.get_numbers(s)
    if not len(numbers):
        return None

    # iteratively attempt to parse the numbers
    for number in numbers:

        # floats
        try:
            return round(float(number), bpm_decimals)
        except ValueError:
            pass

        # ints
        try:
            return float(int(number))
        except ValueError:
            pass

    # give up
    return None


def id3_get_key_fields(raw_tag: str) -> dict:
    f"""
    Get pitch data from a raw_tag:
    {RAW_TAG_PARAM}
    :return dict
    """
    data = {}
    if raw_tag is None or raw_tag.strip() == "":
        return data
    if raw_key:
        raw_key = raw_tag.upper()
        data["is_musical_key_minor"] = raw_key.endswith("M")
        data["musical_root"] = raw_key.replace("M", "")
        data["musical_key"] = (
            dada_settings.AUDIO_DEFAULTS_HARMONIC_CODES_TO_KEYS.get(
                raw_key, dada_settings.AUDIO_DEFAULTS_KEY_LOOKUP.get(raw_key, "")
            )
            .strip()
            .upper()
            .replace("m", "M")
        )
        # TODO: add relative major / minor + 5ths
        data["harmonic_code"] = audio.key_to_harmonic_code(data["musical_key"])
        data["musical_key"] = data["musical_key"].title()
    return data


def id3_get_num_fields(raw_tag: RawId3Tag, type: str = "track") -> Dict[str, Any]:
    f"""
    Get id3 number data (either disc number or track number)
    {RAW_TAG_PARAM}
    :param type: the type of number data to get (either ``track`` or ``disc``)
    :return dict
    """
    data = {}
    if raw_tag is None or raw_tag.strip() == "":
        return data

    numbers = dada_text.get_numbers(raw_tag)

    # select first two numbers
    if len(numbers) > 2:
        numbers = [numbers[0], numbers[1]]

    # number and total (eg: 1/14)
    if len(numbers) == 2:
        return {
            f"{type}_num": int(numbers[0].strip()),
            f"{type}_total": int(numbers[1].strip()),
        }
    # just the number (eg: 1)
    elif len(numbers) == 1:
        return {f"{type}_num": int(numbers[0].strip())}
    return {}


def id3_get_bar_fields(
    fields: dict = {},
    bpm_field: str = "bpm",
    duration_field: str = "duration",
    bar_length: int = 4,
) -> Dict[str, Any]:
    """
    Get number of bars / measures using
    :param fields: a list of processed id3 fields
    :param bpm_field: the name of the bpm field
    :param duration_field: the name of the duration field
    :param bar_length: the name of measures per bar (default: ``4``)
    :return dict
    """
    data = {}
    bpm = fields.get(bpm_field, None)
    duration = fields.get(duration_field, None)
    if bpm is not None and duration is not None:
        data["num_measures"] = get_number_of_measures(bpm, duration)
        data["num_bars"] = get_number_of_bars(bpm, duration, bar_length)
    return data


# ///////////////////
# Lookup of tag name to field name
# TODO: combine this with list of fields?>
# ///////////////////

# Some of the one's i've seen so far:
#  FILEWEBPAGE': ['http://traxsource.com/track/675270/faith-malik-s-drum-and-organ-mix']
#  GENRE': ['Soulful House']
#  INITIALKEY': ['Cm']
#  ORIGINALALBUM': ['Faith - The Remixes']
#  ORIGINALARTIST': ['Veronique']
#  ORIGINALDATE': ['2011-12-02']
#  PUBLISHERWEBPAGE': ['http://traxsource.com/label/5189/truth-manifest-records']
#  RELEASEDATE': ['2011-12-02']
#  TITLE': ['Faith  (Malik’s Drum & Organ Mix)']
#  TRACKNUMBER': ['05']}
# --------------------------
# 'COMMENT:ITUNNORM': [' 0000075D 00000615 00007649 000039BA 0000EEC6 0001127D 00008292 00007837 00000C24 000047BC'],
# 'COMMENT:ITUNPGAP': ['0'],
# 'COMMENT:ITUNSMPB': [' 00000000 00000210 00000870 0000000000647D00 00000000 002D871A 00000000 00000000 00000000 00000000 00000000 00000000'],
# 'COMMENT:UID': ['fbbb21ce3db5ced3e219bb386a942a00'], 'ENCODEDBY': ['iTunes v7.3.2'], 'INITIALKEY': ['F#m'], 'TITLE': ['89.8 (F#) IRAQSPEECHESshort']}
# --------------------------
# 'ENCODING': ['Logic Pro X 10.3.2']}
# ---------------------------
# 'TRACKNUMBER': ['2 The Bone-Everybody']}
# ------------------------------
#  'ORGANIZATION': ['Abora Recordings'],
#  -------------------------------
#  'DISCOGS_ARTIST_LINK': ['100%20Hz'],
# 'DISCOGS_CATALOG': ['OBL 12005'],
# 'DISCOGS_COUNTRY': ['UK'],
# 'DISCOGS_LABEL': ['Oblong Records'],
# 'DISCOGS_LABEL_LINK': ['Oblong%20Records'],
# 'DISCOGS_ORIGINAL_TRACK_NUMBER': ['02'],
# 'DISCOGS_RELEASED': ['2000'],
# 'DISCOGS_RELEASE_ID': ['21217']
# -----------------------------------
# 'ENERGYLEVEL': ['6'],
# -----------------------------------
# 'LANGUAGE': ['eng'], 'RELEASE TYPE': [' '], 'RIP DATE': ['2016-07-17'], 'SOURCE': ['WEB'], 'TITLE': ['The Dreamer (4AM Mix)'], 'TRACKNUMBER': ['5/30'], 'URL': ['http://play.google.com']}
# -----------------------------------
#  'AUTHOR': ['RTGROY'], 'COMMENT': ['www.mediahuman.com'], 'COMPATIBLE_BRANDS': ['isommp42'], 'ENCODING': ['Lavf56.25.101'], 'INITIALKEY': ['Abm'], 'MAJOR_BRAND': ['mp42'], 'MINOR_VERSION':

ID3_FIELDS_TO_RAW_TAGS = {
    "artist_name": {"tag_name": "ARTIST"},
    "composer": {"tag_name": "COMPOSER"},
    "album_artist_name": {"tag_name": "ALBUMARTIST"},
    "original_artist_name": {"tag_name": "ORIGINALARTIST"},
    "label_name": {"tag_name": "LABEL"},
    "track_title": {"tag_name": "TITLE"},
    "album_name": {"tag_name": "ALBUM"},
    "original_album_name": {"tag_name": "ORIGINALALBUM"},
    "webpage": {"tag_name": "FILEWEBPAGE"},
    "organization": {"tag_name": "ORGANIZATION"},
    "publisher_webpage": {"tag_name": "PUBLISHERWEBPAGE"},
    "genre": {"tag_name": "GENRE"},
    "track_num": {
        "tag_name": "TRACK",
        "func": partial(id3_get_num_fields, type="track"),
    },
    "rip_date": {"tag_name": "RIPDATE", "func": id3_clean_date},
    "source": {"tag_name": "SOURCE", "func": id3_clean_date},
    "compilation": {"tag_name": "COMPLIATION"},
    "comment": {"tag_name": "COMMENT", "max_length": 512},
    "encoded_by": {"tag_name": "ENCODEDBY"},
    "uid": {"tag_name": "COMMENT:UID"},
    "discogs_artist_link": {"tag_name": "DISCOGS_ARTIST_LINK"},
    "discogs_label": {"tag_name": "DISCOGS_LABEL"},
    "discogs_catalog": {"tag_name": "DISCOGS_CATALOG"},
    "discogs_country": {"tag_name": "DISCOGS_COUNTRY"},
    "discogs_original_track_num": {
        "tag_name": "DISCOGS_ORIGINAL_TRACK_NUMBER",
        "func": id3_clean_int,
    },
    "year": {"tag_name": "DATE", "func": id3_clean_year},
    "release_date": {"tag_name": "RELEASEDATE", "func": id3_clean_date},
    "original_date": {"tag_name": "ORIGINALDATE", "func": id3_clean_date},
    "discogs_released_year": {"tag_name": "DISCOGS_RELEASED", "func": id3_clean_year},
    "discogs_release_id": {"tag_name": "DISCOGS_RELEASE_ID"},
    "itunes_norm": {"tag_name": "COMMENT:ITUNNORM"},
    "itunes_pgap": {"tag_name": "COMMENT:ITUNPGAP"},
    "itunes_smpb": {"tag_name": "COMMENT:ITUNSMPB"},
    "energy_level": {"tag_name": "ENERGYLEVEL"},
    "lyrics": {"tag_name": "LYRICS"},
    "lyricist": {"tag_name": "LYRICIST"},
    "language": {"tag_name": "LANGUAGE"},
    "url": {"tag_name": "URL"},
    "author": {"tag_name": "AUTHOR"},
    "lyricist": {"tag_name": "LYRICIST"},
    "bpm": {
        "tag_name": "BPM",
        "func": partial(
            id3_clean_bpm, bpm_decimals=dada_settings.AUDIO_DEFAULTS_BPM_DECIMALS
        ),
    },
    "musical_key": {
        "tag_name": "INITIALKEY",
        "fields": True,
        "func": id3_get_key_fields,
    },
    "disc_num": {
        "tag_name": "DISCNUMBER",
        "fields": True,
        "func": partial(id3_get_num_fields, type="disc"),
    },
    "track_num": {
        "tag_name": "TRACKNUMBER",
        "fields": True,
        "func": partial(id3_get_num_fields, type="track"),
    },
}

# TODO set custom tags


# ///////////////////
# Main ID3 Functions
# ///////////////////


def id3_tags_to_fields(tags: dict, defaults: dict = {}) -> dict:
    """
    Convert raw id3 tags into fields
    :param tags: A dictionary of raw id3 tags.
    """
    # standardize input tag names
    tags = {id3_clean_tag_name(k): v for k, v in tags.items()}

    # build up list of fields
    fields = {}
    for field_name, schema in ID3_FIELDS_TO_RAW_TAGS.items():

        value = None
        tag_name = schema["tag_name"]
        # get the raw tag value
        raw_tag = id3_clean_tag(tags.get(id3_clean_tag_name(tag_name), None))

        # attempt to get comment fields without 'COMMENT:' it front of them
        if not raw_tag and tag_name.startswith("COMMENT:"):
            value = id3_clean_tag(
                tags.get(id3_clean_tag_name(tag_name.replace("COMMENT:", "")), None)
            )

        # apply clean function
        clean_fx = schema.get("func", None)
        if clean_fx:
            value = clean_fx(value)

        # format fields
        if schema.get("fields", False):
            if value is not None and isinstance(value, dict):
                fields.update(value)
            else:
                raise ValueError(
                    f"Invalid internal {field_name} format: {value}. Should return a `dict`"
                )

        # set value
        elif value is not None and str(value):
            fields[field_name] = value

    # update defaults
    defaults.update(fields)

    # add bar fields
    bar_fields = id3_get_bar_fields(defaults)
    defaults.update(bar_fields)

    return defaults


def id3_fields_to_tags(fields: dict, prefix: str = "id3") -> Dict[str, str]:
    """
    :param fields: A dictionary of processed fields to convert into id3 tags
    """
    # standardize key names
    fields = {k.replace(f"{prefix}_", ""): v for k, v in fields.items()}

    # build up tags
    tags = {}
    for field_name, schema in audio.ID3_FIELDS_TO_RAW_TAGS.items():
        tag_value = fields.get(field_name, None)
        if tag_value is not None and str(tag_value.strip()) != "":
            if dates.is_date(tag_value):
                tag_value = tag_name.isoformat()
            tags[schema["tag_name"]] = str(tag_value)
    return tags


def id3_extract_fields(
    filepath: str,
    prefix: str = "id3",
    defaults: Dict[str, Any] = {},
    bpm_decimals: int = dada_settings.AUDIO_DEFAULTS_BPM_DECIMALS,
    **kwargs,
) -> Dict[str, Any]:
    f"""
    Parse ID3 Tags from a filepath
    :param filepath: The filepath to fetch the tags from
    :param prefix: a string to prefix all field names with
    :param defaults: default fields to pass into the function.
    {BPM_DECIMALS_PARAM}
    :return dict
    """
    try:
        id3 = taglib.File(filepath)
    except OSError:
        raise ValueError(f"[id3] Could not open file: {filepath}")

    # get base fields
    fields = {
        "duration": id3.length,
        "bit_rate": id3.bitrate,
        "sample_rate": id3.sampleRate,
        "is_stereo": id3.channels == 2,
    }

    # parse id3 tags
    fields = id3_tags_to_fields(id3.tags, fields)

    # overwrite defaults and filter fulls
    return etc.get_fields_data(fields, prefix, defaults)


def id3_set_tags(
    filepath: str,
    fields: Dict[str, Any] = {},
    prefix: str = "id3",
    defaults: Dict[str, Any] = {},
    **kwargs,
) -> str:
    f"""
    Parse ID3 Tags from a filepath
    :param filepath: The filepath to fetch the tags from
    :param fields: fields to map to id3 tags
    :param prefix: a string to prefix all field names with
    :param defaults: default tags pass into the function (eg: ``{"ARTIST":"JON FAY"}`` ).
    :return str
    """
    try:
        id3 = taglib.File(filepath)
    except OSError:
        raise ValueError(f"[id3] Could not open file: {filepath}")

    # parse current id3 fields
    old_fields = id3_tags_to_fields(id3.tags, fields)

    # update old tags with new tags
    old_fields.update(fields)

    # generate tags
    tags = id3_fields_to_tags(fields, prefix)

    # udpate default tags with new tags
    defaults.update(tags)

    # format as lists
    for tag_name, tag_value in defaults.items():
        id3.tags[tag_name] = [str(tag_value)]

    # save tags
    id3.save()
    return filepath
