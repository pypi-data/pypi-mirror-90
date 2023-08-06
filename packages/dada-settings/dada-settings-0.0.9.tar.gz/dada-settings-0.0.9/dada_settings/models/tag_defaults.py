from dada_settings.utils import join_fields

# ///////////////////////////////////////
# Default TAG Generation
# ///////////////////////////////////////

# DEFAULT TAGS
TAG_DEFAULTS = [
    {"name": "globally-ltd", "info": "content related to globally.ltd"},
]


# /////////////////
# DEFAULT TAG FIELDS
# ////////////////

TAG_DEFAULTS_DEFAULT_FIELD_PROPS = {
    "accepts_entity_types": ["tag"],
    "accepts_file_types": ["all"],
}

TAG_DEFAULTS_DEFAULT_FIELDS_INIT = [
    {
        "name": "assoicated_url",
        "type": "url",
        "info": "A url associated with a website",
    },
]

TAG_DEFAULTS_DEFAULT_FIELDS = join_fields(
    "tag", TAG_DEFAULTS_DEFAULT_FIELDS_INIT, TAG_DEFAULTS_DEFAULT_FIELD_PROPS
)
