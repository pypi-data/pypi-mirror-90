from dada_settings.utils import join_fields

# ///////////////////////////////////////
# Default Desktop Generation
# ///////////////////////////////////////

# DEFAULT DESKTOPS
DESKTOP_DEFAULTS = [
    {"name": "dev", "info": "Your default, private environment", "is_private": True,},
    {"name": "shared", "info": "Your public environment", "is_private": False,},
]

DESKTOP_DEFAULTS_DEFAULT_DESKTOP_NAMES = [f["name"] for f in DESKTOP_DEFAULTS]
DESKTOP_DEFAULTS_NUMBER_DEFAULT_DESKTOPS = len(DESKTOP_DEFAULTS_DEFAULT_DESKTOP_NAMES)


DESKTOP_DEFAULTS_DEFAULT_FIELDS = []
