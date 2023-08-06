from dada_settings.utils import join_fields

BUNDLE_DEFAULTS = []


# /////////////////
# DEFAULT BUNDLE FIELDS
# ////////////

BUNDLE_DEFAULTS_DEFAULT_FIELD_PROPS = {
    "accepts_entity_types": ["file"],
    "accepts_file_types": ["bundle"],
    "accepts_file_subtypes": ["all"],
}

BUNDLE_DEFAULTS_DEFAULT_FIELDS_INIT = [{"name": "contents", "type": "text_array"}]

BUNDLE_DEFAULTS_DEFAULT_FIELDS = join_fields(
    "bundle", BUNDLE_DEFAULTS_DEFAULT_FIELDS_INIT, BUNDLE_DEFAULTS_DEFAULT_FIELD_PROPS
)
