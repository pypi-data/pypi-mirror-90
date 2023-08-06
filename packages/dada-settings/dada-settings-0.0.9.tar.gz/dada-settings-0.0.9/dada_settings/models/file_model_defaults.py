from dada_settings.utils import join_fields

# /////////////////
# DEFAULT MODEL FIELDS
# ////////////////

MODEL_DEFAULTS_DEFAULT_FIELD_PROPS = {
    "accepts_entity_types": ["file"],
    "accepts_file_types": ["model"],
}

MODEL_DEFAULTS_DEFAULT_FIELDS_INIT = [
    {
        "name": "num_layers",
        "type": "int",
        "info": "The number of layers in this model",
    },
]

MODEL_DEFAULTS_DEFAULT_FIELDS = join_fields(
    "model", MODEL_DEFAULTS_DEFAULT_FIELDS_INIT, MODEL_DEFAULTS_DEFAULT_FIELD_PROPS
)
