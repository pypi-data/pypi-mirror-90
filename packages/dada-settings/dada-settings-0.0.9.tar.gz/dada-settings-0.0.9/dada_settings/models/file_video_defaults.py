from dada_settings.utils import join_fields

# /////////////////
# DEFAULT VIDEO FIELDS
# ////////////////

VIDEO_DEFAULTS_DEFAULT_FIELD_PROPS = {
    "accepts_entity_types": ["file"],
    "accepts_file_types": ["video"],
}

VIDEO_DEFAULTS_DEFAULT_FIELDS_INIT = [
    # toplevel information
    {"name": "video_has_audio", "type": "bool"},
    {"name": "probe_score", "type": "int"},
    {"name": "format_name", "type": "text", "is_searchable": True},
    {"name": "created_date", "type": "date"},
    # video-specific attributes
    {"name": "video_codec_name", "type": "text"},
    {"name": "video_color_range", "type": "text"},
    {"name": "video_width", "type": "smallint"},
    {"name": "video_height", "type": "smallint"},
    {"name": "video_level", "type": "int"},
    {"name": "video_bit_rate", "type": "int"},
    {"name": "video_duration", "type": "num"},
    {"name": "video_start_time", "type": "num"},
    {"name": "video_nb_frames", "type": "int"},
    {"name": "sample_aspect_ratio_x", "type": "smallint"},
    {"name": "sample_aspect_ratio_y", "type": "smallint"},
    {"name": "display_aspect_ratio_x", "type": "smallint"},
    {"name": "display_aspect_ratio_y", "type": "smallint"},
    {"name": "avg_frame_rate", "type": "num"},
    # audio-specific attributes
    {"name": "audio_codec_name", "type": "text"},
    {"name": "audio_is_stereo", "type": "bool"},
    {"name": "audio_sample_rate", "type": "int"},
    {"name": "audio_bit_rate", "type": "int"},
    {"name": "audio_nb_frames", "type": "int"},
    {"name": "audio_language", "type": "text"},
    # audio dipositions
    {"name": "audio_disposition_is_default", "type": "bool"},
    {"name": "audio_disposition_is_dub", "type": "bool"},
    {"name": "audio_disposition_is_original", "type": "bool"},
    {"name": "audio_disposition_is_comment", "type": "bool"},
    {"name": "audio_disposition_is_lyrics", "type": "bool"},
    {"name": "audio_disposition_is_karaoke", "type": "bool"},
    {"name": "audio_disposition_is_forced", "type": "bool"},
    {"name": "audio_disposition_is_hearing_impaired", "type": "bool"},
    {"name": "audio_disposition_is_visual_impaired", "type": "bool"},
    {"name": "audio_disposition_is_clean_effects", "type": "bool"},
    {"name": "audio_disposition_is_attached_pic", "type": "bool"},
    {"name": "audio_disposition_is_timed_thumbnails", "type": "bool"},
]

VIDEO_DEFAULTS_DEFAULT_FIELDS = join_fields(
    "ffp", VIDEO_DEFAULTS_DEFAULT_FIELDS_INIT, VIDEO_DEFAULTS_DEFAULT_FIELD_PROPS
)
