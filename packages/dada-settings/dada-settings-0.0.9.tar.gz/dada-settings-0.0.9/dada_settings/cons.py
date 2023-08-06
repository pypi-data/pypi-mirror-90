#############
# constants #
#############

# fields
from dada_settings.constants.field_defaults import *


# files
from dada_settings.constants.file_defaults import *
from dada_settings.constants.file_bundle_defaults import *
from dada_settings.constants.file_code_defaults import *
from dada_settings.constants.file_audio_defaults import *
from dada_settings.constants.file_data_defaults import *
from dada_settings.constants.file_doc_defaults import *
from dada_settings.constants.file_model_defaults import *
from dada_settings.constants.file_image_defaults import *
from dada_settings.constants.file_video_defaults import *
from dada_settings.constants.file_store_defaults import *

# etc
from dada_settings.constants.tag_defaults import *
from dada_settings.constants.theme_defaults import *

##################
# model defaults #
##################

# files
from dada_settings.models.file_bundle_defaults import *
from dada_settings.models.file_defaults import *
from dada_settings.models.file_code_defaults import *
from dada_settings.models.file_data_defaults import *
from dada_settings.models.file_doc_defaults import *
from dada_settings.models.file_audio_defaults import *
from dada_settings.models.file_image_defaults import *
from dada_settings.models.file_video_defaults import *
from dada_settings.models.file_model_defaults import *

# etc
from dada_settings.models.user_defaults import *
from dada_settings.models.tag_defaults import *
from dada_settings.models.desktop_defaults import *
from dada_settings.models.folder_defaults import *

#############################
# field generation defaults #
#############################

# gen defaults
from dada_settings.gen.desktop_defaults import *
from dada_settings.gen.field_defaults import *
from dada_settings.gen.folder_defaults import *


#####################################
# File extension / mimetype lookups #
#####################################


FILE_VALID_TYPE_EXT_MIMETYPE = {
    "audio": AUDIO_DEFAULTS_VALID_EXT_MIMETYPE,
    "video": VIDEO_DEFAULTS_VALID_EXT_MIMETYPE,
    "image": IMAGE_DEFAULTS_VALID_EXT_MIMETYPE,
    "model": MODEL_DEFAULTS_VALID_EXT_MIMETYPE,
    "bundle": BUNDLE_DEFAULTS_VALID_EXT_MIMETYPE,
    "data": DATA_DEFAULTS_VALID_EXT_MIMETYPE,
    "code": CODE_DEFAULTS_VALID_EXT_MIMETYPE,
    "doc": DOC_DEFAULTS_VALID_EXT_MIMETYPE,
    "raw": {},
}


def _rev(d):
    return {v: k for k, v in d.items()}


FILE_VALID_TYPE_MIMETYPE_EXT = {
    "audio": _rev(AUDIO_DEFAULTS_VALID_EXT_MIMETYPE),
    "video": _rev(VIDEO_DEFAULTS_VALID_EXT_MIMETYPE),
    "image": _rev(IMAGE_DEFAULTS_VALID_EXT_MIMETYPE),
    "model": _rev(MODEL_DEFAULTS_VALID_EXT_MIMETYPE),
    "bundle": _rev(BUNDLE_DEFAULTS_VALID_EXT_MIMETYPE),
    "data": _rev(DATA_DEFAULTS_VALID_EXT_MIMETYPE),
    "code": _rev(CODE_DEFAULTS_VALID_EXT_MIMETYPE),
    "doc": _rev(DOC_DEFAULTS_VALID_EXT_MIMETYPE),
    "raw": _rev({}),
}

FILE_VALID_EXT_MIMETYPE = {
    kk: vv for k, v in FILE_VALID_TYPE_EXT_MIMETYPE.items() for kk, vv in v.items()
}

FILE_VALID_MIMETYPE_EXT = {
    kk: vv for k, v in FILE_VALID_TYPE_MIMETYPE_EXT.items() for kk, vv in v.items()
}

# ###########################################
# Default Fields by entity type / file type #
# ###########################################

FIELD_TYPE_DEFAULTS = {
    "file": {
        "audio": AUDIO_DEFAULTS_DEFAULT_FIELDS,
        "bundle": BUNDLE_DEFAULTS_DEFAULT_FIELDS,
        "code": CODE_DEFAULTS_DEFAULT_FIELDS,
        "doc": DOC_DEFAULTS_DEFAULT_FIELDS,
        "data": DATA_DEFAULTS_DEFAULT_FIELDS,
        "image": IMAGE_DEFAULTS_DEFAULT_FIELDS,
        "model": MODEL_DEFAULTS_DEFAULT_FIELDS,
        "video": VIDEO_DEFAULTS_DEFAULT_FIELDS,
        "raw": [],
    },
    "desktop": DESKTOP_DEFAULTS_DEFAULT_FIELDS,
    "folder": FOLDER_DEFAULTS_DEFAULT_FIELDS,
    "tag": TAG_DEFAULTS_DEFAULT_FIELDS,
    "user": USER_DEFAULTS_DEFAULT_FIELDS,
}

# construct list of default fields
FIELD_DEFAULTS = []
for k, v in FIELD_TYPE_DEFAULTS.items():
    if isinstance(v, dict):
        for kk, vv in v.items():
            FIELD_DEFAULTS.extend(vv)
    else:
        FIELD_DEFAULTS.extend(v)

FIELD_DEFAULT_NAMES = [v["name"] for v in FIELD_DEFAULTS if "name" in v]
