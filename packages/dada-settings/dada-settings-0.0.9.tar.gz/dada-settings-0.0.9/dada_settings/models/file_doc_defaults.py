from dada_settings.utils import join_fields

# /////////////////
# DEFAULT DOC FIELDS
# ////////////////

DOC_DEFAULTS_DEFAULT_FIELD_PROPS = {
    "accepts_entity_types": ["file"],
    "accepts_file_types": ["doc"],
}

DOC_DEFAULTS_DEFAULT_FIELDS_INIT = [
    {
        "name": "text_contents",
        "type": "text",
        "info": "The document's extracted text contents",
        "is_searchable": True,
    },
]

DOC_DEFAULTS_DEFAULT_FIELDS = join_fields(
    "doc", DOC_DEFAULTS_DEFAULT_FIELDS_INIT, DOC_DEFAULTS_DEFAULT_FIELD_PROPS
)
