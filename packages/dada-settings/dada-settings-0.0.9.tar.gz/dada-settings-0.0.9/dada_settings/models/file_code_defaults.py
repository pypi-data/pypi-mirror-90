from dada_settings.utils import join_fields

# /////////////////
# DEFAULT CODE FIELDS
# ////////////////

CODE_DEFAULTS_DEFAULT_FIELD_PROPS = {
    "accepts_entity_types": ["file"],
    "accepts_file_types": ["code"],
}

CODE_DEFAULTS_DEFAULT_FIELDS_INIT = [
    {"name": "language", "type": "text", "info": "The inferred programming language",},
]

CODE_DEFAULTS_DEFAULT_FIELDS = join_fields(
    "code", CODE_DEFAULTS_DEFAULT_FIELDS_INIT, CODE_DEFAULTS_DEFAULT_FIELD_PROPS
)
