import os

from dada_settings.utils import join_fields


# super user
SUPER_USER_NAME = os.getenv("DADA_SUPER_USER_NAME", "gltd")
SUPER_USER_EMAIL = os.getenv("DADA_SUPER_USER_EMAIL", "dev@globally.ltd")
SUPER_USER_PASSWORD = os.getenv("DADA_SUPER_USER_PASSWORD", "dada")
SUPER_USER_API_KEY = os.getenv("DADA_SUPER_USER_API_KEY", "dev")

# default users
USER_DEFAULTS = [
    {
        "name": SUPER_USER_NAME,
        "email": SUPER_USER_EMAIL,
        "password": SUPER_USER_PASSWORD,
        "api_key": SUPER_USER_API_KEY,
        "fields": {"settings": {"is_default": True}},
    }
]

# /////////////////
# DEFAULT USER FIELDS
# ////////////////

USER_DEFAULTS_DEFAULT_FIELD_PROPS = {
    "accepts_entity_types": ["user"],
}

USER_DEFAULTS_DEFAULT_FIELDS_INIT = [
    {"name": "settings", "type": "json", "info": "Arbitrary user settings",},
]

USER_DEFAULTS_DEFAULT_FIELDS = join_fields(
    "user", USER_DEFAULTS_DEFAULT_FIELDS_INIT, USER_DEFAULTS_DEFAULT_FIELD_PROPS
)
