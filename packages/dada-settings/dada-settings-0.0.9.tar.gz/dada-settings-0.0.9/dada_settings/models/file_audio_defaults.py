from dada_settings.utils import join_fields

# /////////////////
# DEFAULT AUDIO FIELDS
# ////////////
AUDIO_DEFAULTS_DEFAULT_FIELD_PROPS = {
    "accepts_entity_types": ["file"],
    "accepts_file_types": ["audio"],
}

# TODO: Move this to an EXTRACT TASK!
AUDIO_DEFAULTS_DEFAULT_FIELDS_INIT = [
    # /////////////////
    # ID3 TAGS
    # ////////////
    # SEARCHABLE
    {"name": "artist_name", "type": "text", "is_searchable": True},
    {"name": "original_artist_name", "type": "text"},
    {"name": "album_artist_name", "type": "text"},
    {"name": "track_title", "type": "text", "is_searchable": True},
    {"name": "album_name", "type": "text", "is_searchable": True},
    {"name": "original_album_name", "type": "text"},
    {"name": "genre", "type": "text"},
    {"name": "label_name", "type": "text"},
    {"name": "comment", "type": "text"},
    {"name": "encoded_by", "type": "text"},
    # Integers
    {"name": "bit_rate", "type": "int"},
    {"name": "sample_rate", "type": "int"},
    {"name": "track_num", "type": "int"},
    {"name": "track_total", "type": "int"},
    {"name": "disc_num", "type": "int"},
    {"name": "disc_total", "type": "int"},
    {"name": "bytes", "type": "int"},
    {"name": "year", "type": "int"},
    {"name": "compilation", "type": "int"},
    {"name": "num_measures", "type": "int"},
    {"name": "num_bars", "type": "int"},
    # Dates
    {"name": "release_date", "type": "date_tz"},
    {"name": "original_date", "type": "date_tz"},
    # URLs (not type enforced)
    {"name": "webpage", "type": "text"},
    {"name": "publisher_webpage", "type": "text"},
    {"name": "url", "type": "text"},
    # Numeric
    {"name": "bpm", "type": "num"},
    {"name": "duration", "type": "num"},
    # Boolean
    {"name": "is_stereo", "type": "bool"},
    # ENUM
    {
        "name": "musical_key",
        "type": "text",
        # "options": AUDIO_DEFAULTS_VALID_KEYS, # TODO: Figure out this bug
    },
    {
        "name": "harmonic_code",
        "type": "text",
        # "options": AUDIO_DEFAULTS_VALID_HARMONIC_CODES, # TODO: Figure out this bug
    },
]

AUDIO_DEFAULTS_DEFAULT_FIELDS = join_fields(
    "id3", AUDIO_DEFAULTS_DEFAULT_FIELDS_INIT, AUDIO_DEFAULTS_DEFAULT_FIELD_PROPS
)
