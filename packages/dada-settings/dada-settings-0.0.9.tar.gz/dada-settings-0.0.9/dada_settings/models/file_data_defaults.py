from dada_settings.utils import join_fields

# /////////////////
# DEFAULT DATA FIELDS
# ////////////////

DATA_DEFAULTS_DEFAULT_FIELD_PROPS = {
    "accepts_entity_types": ["file"],
    "accepts_file_types": ["data"],
}

DATA_DEFAULTS_DEFAULT_FIELDS_INIT = [
    {"name": "n_rows", "type": "int", "info": "The number of rows in the dataset",},
    {"name": "n_cols", "type": "int", "info": "The number of columns in the dataset",},
    {"name": "dada_schema", "type": "json", "info": "The inferred dada schema",},
]

DATA_DEFAULTS_DEFAULT_FIELDS = join_fields(
    "data", DATA_DEFAULTS_DEFAULT_FIELDS_INIT, DATA_DEFAULTS_DEFAULT_FIELD_PROPS
)
