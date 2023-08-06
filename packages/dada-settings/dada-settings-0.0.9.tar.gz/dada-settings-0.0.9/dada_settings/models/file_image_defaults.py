from dada_settings.utils import join_fields

# /////////////////
# DEFAULT IMAGE FIELDS
# /////////////////

IMAGE_DEFAULTS_DEFAULT_FIELD_PROPS = {
    "accepts_entity_types": ["file"],
    "accepts_file_types": ["image"],
}

IMAGE_DEFAULTS_DEFAULT_FIELDS_INIT = [
    # /////////////////
    # EXIF DATA
    # ////////////////
    {"name": "artist", "type": "text", "is_searchable": True},
    {"name": "info", "type": "text", "is_searchable": True},
    {"name": "date_time", "type": "date"},
    {"name": "camera_make", "type": "text"},
    {"name": "camera_model", "type": "text"},
    {"name": "image_width", "type": "int"},
    {"name": "image_height", "type": "int"},
    {"name": "x_resolution", "type": "int_array"},
    {"name": "y_resolution", "type": "int_array"},
    {"name": "camera_owner_name", "type": "text_256", "is_searchable": True},
    {"name": "flash", "type": "smallint"},
    {"name": "color_space", "type": "smallint"},
    {"name": "exposure_time", "type": "int_array"},
    # # photo settings
    # { 'name': 'shutter_speed_value', 'type': 'int_array'},
    # { 'name': 'aperture_value', 'type': 'int_array'},
    # { 'name': 'exposure_bias_value', 'type': 'int_array'},
    # { 'name': 'max_aperture_value', 'type': 'int_array'},
    # { 'name': 'metering_mode', "type": "smallint"},
    # { 'name': 'focal_length', 'type': 'int_array'},
    # { 'name': 'compressed_bits_per_pixel', 'type': 'int_array'},
    # # { 'name': 'date_time_original', 'type': 'date'},
    # # { 'name': 'date_time_digitized', 'type': 'date'},
    # { 'name': 'color_space', "type": "smallint"},
    # { 'name': 'focal_plane_x_resolution', 'type': 'int_array'},
    # { 'name': 'subsec_time', "type": "smallint"},
    # # { 'name': 'subsec_time_original', "type": "smallint"},
    # # { 'name': 'subsec_time_digitized', "type": "smallint"},
    # { 'name': 'focal_plane_y_resolution', 'type': 'int_array'},
    # # { 'name': 'focal_plane_resolution_unit', "type": "smallint"},
    # { 'name': 'sensing_method', "type": "smallint"},
    # { 'name': 'interoperability_offset', "type": "smallint"},
    # { 'name': 'f_number', 'type': 'int_array'},
    # { 'name': 'copyright', 'type': 'text_256'},
    # { 'name': 'exposure_program', "type": "smallint"},
    # { 'name': 'custom_rendered', "type": "smallint"},
    # { 'name': 'iso_speed_ratings', "type": "smallint"},
    # { 'name': 'resolution_unit', "type": "smallint"},
    # { 'name': 'exposure_mode', "type": "smallint"},
    # { 'name': 'white_balance', "type": "smallint"},
    # { 'name': 'body_serial_number', 'type': "text"},
    # { 'name': 'digital_zoom_ratio', 'type': 'int_array' 5472, 5472),
    # { 'name': 'scene_capture_type', "type": "smallint"},
    # { 'name': 'orientation', "type": "smallint"},
    # { 'name': 'offset', "type": "smallint"},
    # { 'name': 'y_cb_cr_positioning', "type": "smallint"},
    # /////////////////
    # OTHER DATA
    # ////////////////
    # ...
]

IMAGE_DEFAULTS_DEFAULT_FIELDS = join_fields(
    "exif", IMAGE_DEFAULTS_DEFAULT_FIELDS_INIT, IMAGE_DEFAULTS_DEFAULT_FIELD_PROPS
)
