BUNDLE_DEFAULTS_VALID_EXT_MIMETYPE = {
    "tar": "application/x-tar",
    "Z": "application/zip",
    "zip": "application/zip",
    "gzip": "application/gzip",
    "gz": "application/gzip",
    "7z": "application/x-7z-compressed",
    "rar": "application/vnd.rar",
    "bz": "application/x-bzip",
    "bz2": "application/x-bzip2",
}
BUNDLE_DEFAULTS_VALID_EXT = list(BUNDLE_DEFAULTS_VALID_EXT_MIMETYPE.keys())


# //
# Heuristics for detecting whether a bundle
# is of a particular subtype
# //
BUNDLE_DEFAULTS_GUESS_SUBTYPE_FROM_EXTENSTIONS = {
    "gltf": {
        "ext_must": ["gltf"],
        "ext_possible": ["gltf", "png", "jpg", "bin"],
        "dir_possible": ["textures"],
        "min_files": 1,
        "max_files": 20,
        "max_dir_depth": 2,
    },
    "ableton_project": {
        "pkg_endswith": ["Project"],
        "ext_must": ["als"],
        "ext_possible": ["wav", "mp3", "aif", "aiff", "m4a", "flac", "mp4", "mov"],
        "dir_possible": ["Samples", "Backup", "Ableton Project Info"],
        "min_files": 1,
    },
    "logic_project": {
        "pkg_endswith": ["logicx"],
        "ext_possible": [
            "logicx",
            "wav",
            "mp3",
            "aif",
            "aiff",
            "m4a",
            "flac",
            "mp4",
            "mov",
        ],
        "dir_possible": ["alternatives", "contents", "media", "resources"],
        "min_files": 1,
    },
    "git_repo": {
        "ext_possible": ["md", "py", "js", "yml", "R", "css", "html",],
        "dir_possible": [".git"],
        "min_files": 1,
    },
    "audio_album": {
        "ext_must": ["als"],
        "ext_possible": [
            "wav",
            "mp3",
            "aif",
            "aiff",
            "bin",
            "m4a",
            "flac",
            "mp4",
            "mov",
        ],
        "dir_possible": [
            "mp3",
            "wav",
            "aiff",
            "aif",
            "m4a",
            "flac",
        ],  # eg album/mp3/file1.mp3
        "path_possible": ["cover.png", "cover.jpg", "cover.jpeg"],
        "min_files": 1,
        "max_dir_depth": 2,
    },
    "rekordbox_library": {
        "ext_must": ["xml"],
        "ext_possible": ["wav", "mp3", "aif", "m4a", "flac", "aiff"],
        "min_files": 1,
        "max_dir_depth": 2,
    },
    "itunes_library": {
        "ext_must": ["xml"],
        "ext_possible": [
            "wav",
            "mp3",
            "aif",
            "m4a",
            "flac",
            "aiff",
            "jpg",
            "png",
            "jpeg",
            "mov",
            "mp4",
        ],
        "dir_possible": ["music"],
        "path_possible": ["library.xml"],
        "min_files": 1,
        "max_dir_depth": 2,
    },
}

BUNDLE_DEFAULTS_SUBTYPES = [
    "gltf",
    "ableton_project",
    "logic_project",
    "git_repo",
    "audio_album",
    "rekordbox_library",
    "itunes_library",
    # TODO: MORE!
]
