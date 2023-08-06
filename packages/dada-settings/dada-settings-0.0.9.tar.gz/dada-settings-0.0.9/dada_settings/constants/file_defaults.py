import os

# ///////////////////////////////////////
# Env Configurations
# ///////////////////////////////////////


FILE_DEFAULTS_NUMBER_RANDOM_FILES = os.getenv(
    "DADA_FILE_DEFAULTS_NUMBER_RANDOM_FILES", 200
)

FILE_DEFAULTS_NUMBER_DEFAULT_FILES = os.getenv(
    "DADA_FILE_DEFAULTS_NUMBER_DEFAULT_FILES", 20
)

FILE_DEFAULTS_NUMBER_DEFAULT_FIELDS_PER_FILE = os.getenv(
    "DADA_FILE_DEFAULTS_NUMBER_DEFAULT_FIELDS_PER_FILE", 10
)

# ///////////////////////////////////////
# Default Files
# ///////////////////////////////////////


FILE_DEFAULTS_FILE_FIXTURE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "assets")
)
FILE_DEFAULTS_FILE_FIXTURE_1 = os.path.join(
    FILE_DEFAULTS_FILE_FIXTURE_DIR, "audio/tracks/space-time-motion.mp3"
)
FILE_DEFAULTS_FILE_FIXTURE_2 = os.path.join(
    FILE_DEFAULTS_FILE_FIXTURE_DIR, "assets/audio/tracks/eril-brinh2.mp3"
)

FILE_DEFAULTS_FILE_FIXTURES = [
    FILE_DEFAULTS_FILE_FIXTURE_1,
    FILE_DEFAULTS_FILE_FIXTURE_2,
]

# ///////////////////////////////////////
# File type schema
# ///////////////////////////////////////


FILE_DEFAULTS_FILE_TYPES = [
    "audio",
    "bundle",
    "video",
    "image",
    "model",
    "data",
    "doc",
    "code",
    "raw",
]
FILE_DEFAULTS_FILE_TYPES_ALL = FILE_DEFAULTS_FILE_TYPES + ["all"]
FILE_DEFAULTS_DEFAULT_TYPE = "raw"
FILE_DEFAULTS_FILE_SUBTYPE_SCHEMA = {
    "audio": ["hit", "loop", "track", "mix", "raw", "midi"],
    "bundle": [
        "gltf",
        "ableton_project",
        "logic_project",
        "git_repo",
        "audio_album",
        "rekordbox_library",
        "itunes_library",
        "site",
        "app",
        "raw",
    ],
    "video": ["loop", "clip", "raw"],  # TODO add more here
    "image": ["loop", "static", "raw"],  # TODO Add more here
    "model": ["3d"],  # TODO Add more here
    "data": ["raw"],
    "code": ["raw"],
    "raw": ["raw"],
}

FILE_DEFAULTS_FILE_SUBTYPES = list(
    set(
        [val for values in FILE_DEFAULTS_FILE_SUBTYPE_SCHEMA.values() for val in values]
    )
)
FILE_DEFAULTS_FILE_SUBTYPES_ALL = FILE_DEFAULTS_FILE_SUBTYPES + ["all"]
FILE_DEFAULTS_DEFAULT_SUBTYPE = "raw"
FILE_DEFAULTS_DEFAULT_FILE_SUBTYPE_FOR_FILE_TYPE = {
    "audio": "track",
    "bundle": "raw",
    "data": "raw",
    "video": "clip",
    "image": "static",
    "model": "3d",
    "doc": "raw",
    "code": "raw",
    "raw": "raw",
}

FILE_DEFAULTS_DEFAULT_FILE_TYPE = "raw"
FILE_DEFAULTS_DEFAULT_FILE_SUBTYPE = "raw"
FILE_DEFAULTS_DEFAULT_EXT = ""
FILE_DEFAULTS_DEFAULT_MIMETYPE = "application/octet-stream"
