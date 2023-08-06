import random

from dada_settings.utils import join_fields

from dada_settings.models.desktop_defaults import (
    DESKTOP_DEFAULTS_NUMBER_DEFAULT_DESKTOPS,
)

# ///////////////////////////////////////
# Default Folder Generation
# ///////////////////////////////////////


def gen_desktop():
    """"""
    return [random.choice(range(1, DESKTOP_DEFAULTS_NUMBER_DEFAULT_DESKTOPS + 1, 1))]


FOLDER_DEFAULTS = [
    {
        "name": "to_dj",
        "emoji": "heavy_division_sign",
        "info": "Your dj inbox",
        "is_private": True,
        "desktop_id": gen_desktop(),
    },
    {
        "name": "inbox",
        "emoji": "inbox_tray",
        "info": "Stuff to organize",
        "is_private": True,
        "desktop_id": gen_desktop(),
    },
    {
        "name": "to_share",
        "emoji": "link",
        "info": "Stuff to share",
        "is_private": False,
        "desktop_id": gen_desktop(),
    },
]

FOLDER_DEFAULTS_NAMES = [f["name"] for f in FOLDER_DEFAULTS]
FOLDER_DEFAULTS_NUMBER_DEFAULT_FOLDERS = len(FOLDER_DEFAULTS_NAMES)


FOLDER_DEFAULTS_DEFAULT_FIELDS = []
