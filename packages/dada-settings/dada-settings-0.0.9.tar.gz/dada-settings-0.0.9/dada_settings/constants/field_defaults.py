import os

# ///////////////////////////////////////
# Env Configurations
# ///////////////////////////////////////


FIELD_DEFAULTS_FIELD_TABLE_SCHEMA = os.getenv(
    "DADA_FIELD_DEFAULTS_FIELD_TABLE_SCHEMA", "fields"
)

FIELD_DEFAULTS_FIELD_TABLE_PREFIX = os.getenv(
    "DADA_FIELD_DEFAULTS_FIELD_TABLE_SCHEMA", "file_field"
)

# ///////////////////////////////////////
# Search Configuration
# ///////////////////////////////////////

FIELD_DEFAULTS_SEARCHABLE_FIELD_SUFFIX = "vector"

# ///////////////////////////////////////
# FIELD ACCEPTS ENTITY TYPES
# ///////////////////////////////////////

FIELD_DEFAULTS_ENTITY_TYPES = [
    "file",
    "folder",
    "file_folder",
    "folder_desktop",
    "desktop",
    "tag",
    "user",
]
