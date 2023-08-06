# /////////////////
# FILE EXTENSIONS
# /////////////////

AUDIO_DEFAULTS_VALID_EXT_MIMETYPE = {
    "au": "audio/basic",
    "snd": "audio/basic",
    "mp2": "audio/mpeg",
    "mp3": "audio/mpeg",
    "m4a": "audio/x-aiff",
    "aif": "audio/x-aiff",
    "aifc": "audio/x-aiff",
    "aiff": "audio/x-aiff",
    "m3u": "audio/x-mpegurl",
    "m3u8": "audio/x-mpegurl",
    "ra": "audio/vnd.rn-realaudio",
    "ram": "audio/vnd.rn-realaudio",
    "ogg": "audio/ogg",
    "oga": "audio/ogg",
    "wav": "audio/vnd.wav",
    "wave": "audio/vnd.wav",
    "opus": "audio/opus",
    "mid": "audio/midi",
    "midi": "audio/midi",
}

# /////////////////
# KEYS
# /////////////////


AUDIO_DEFAULTS_HARMONIC_CODES_TO_KEYS = {
    "1A": "Abm",
    "2A": "Ebm",
    "3A": "Bbm",
    "4A": "Fm",
    "5A": "Cm",
    "6A": "Gm",
    "7A": "Dm",
    "8A": "Am",
    "9A": "Em",
    "10A": "Bm",
    "11A": "F#m",
    "12A": "Dbm",
    "1B": "B",
    "2B": "F#",
    "3B": "Db",
    "4B": "Ab",
    "5B": "Eb",
    "6B": "Bb",
    "7B": "F",
    "8B": "C",
    "9B": "G",
    "10B": "D",
    "11B": "A",
    "12B": "E",
}

AUDIO_DEFAULTS_KEYS_TO_HARMONIC_CODES = {
    value: key for key, value in AUDIO_DEFAULTS_HARMONIC_CODES_TO_KEYS.items()
}
AUDIO_DEFAULTS_VALID_KEYS = list(AUDIO_DEFAULTS_HARMONIC_CODES_TO_KEYS.values())
AUDIO_DEFAULTS_VALID_HARMONIC_CODES = list(AUDIO_DEFAULTS_HARMONIC_CODES_TO_KEYS.keys())


# lookup of various key formats to Simplified
AUDIO_DEFAULTS_KEY_LOOKUP = {
    "AMAJOR": "A",
    "AMINOR": "Am",
    "A#MAJOR": "Bb",
    "A#MINOR": "Bbm",
    "BBMAJOR": "Bb",
    "BBMINOR": "Bbm",
    "BMAJOR": "B",
    "BMINOR": "Bm",
    "CMAJOR": "C",
    "CMINOR": "Cm",
    "C#MAJOR": "Db",
    "C#MINOR": "Dbm",
    "DBMAJOR": "Db",
    "DBMINOR": "Dbm",
    "DMAJOR": "D",
    "DMINOR": "Dm",
    "D#MAJOR": "Eb",
    "D#MINOR": "Ebm",
    "EBMAJOR": "Eb",
    "EBMINOR": "Ebm",
    "EMAJOR": "E",
    "EMINOR": "Em",
    "FMAJOR": "F",
    "FMINOR": "Fm",
    "F#MAJOR": "F#",
    "F#MINOR": "F#m",
    "GBMAJOR": "F#",
    "GBMINOR": "F#m",
    "GMAJOR": "G",
    "GMINOR": "Gm",
    "G#MAJOR": "Ab",
    "G#MINOR": "Abm",
    "ABMAJOR": "Ab",
    "ABMINOR": "Abm",
    ###
    "AMAJ": "A",
    "AMIN": "Am",
    "A#MAJ": "Bb",
    "A#MIN": "Bbm",
    "BBMAJ": "Bb",
    "BBMIN": "Bbm",
    "BMAJ": "B",
    "BMIN": "Bm",
    "CMAJ": "C",
    "CMIN": "Cm",
    "C#MAJ": "Db",
    "C#MIN": "Dbm",
    "DBMAJ": "Db",
    "DBMIN": "Dbm",
    "DMAJ": "D",
    "DMIN": "Dm",
    "D#MAJ": "Eb",
    "D#MIN": "Ebm",
    "EBMAJ": "Eb",
    "EBMIN": "Ebm",
    "EMAJ": "E",
    "EMIN": "Em",
    "FMAJ": "F",
    "FMIN": "Fm",
    "F#MAJ": "F#",
    "F#MIN": "F#m",
    "GBMAJ": "F#",
    "GBMIN": "F#m",
    "GMAJ": "G",
    "GMIN": "Gm",
    "G#MAJ": "Ab",
    "G#MIN": "Abm",
    "ABMAJ": "Ab",
    "ABMIN": "Abm",
    ###
    "A": "A",
    "AM": "Am",
    "A#": "Bb",
    "A#M": "Bbm",
    "BB": "Bb",
    "BBM": "Bbm",
    "B": "B",
    "BM": "Bm",
    "C": "C",
    "CM": "Cm",
    "C#": "Db",
    "C#M": "Dbm",
    "DB": "Db",
    "DBM": "Dbm",
    "D": "D",
    "DM": "Dm",
    "EB": "Eb",
    "EBM": "Ebm",
    "EB": "Eb",
    "EBM": "Ebm",
    "E": "E",
    "EM": "Em",
    "F": "F",
    "FM": "Fm",
    "F#": "F#",
    "F#M": "F#m",
    "GB": "F#",
    "GBM": "F#m",
    "G": "G",
    "GM": "Gm",
    "G#": "Ab",
    "G#M": "Abm",
    "AB": "Ab",
    "ABM": "Abm",
    "AB": "Ab",
    "ABM": "Abm",
}

# /////////////////
# BPM
# ////////////


AUDIO_DEFAULTS_VALID_BPM_MIN = 20.0
AUDIO_DEFAULTS_VALID_BPM_MAX = 300.0
AUDIO_DEFAULTS_BPM_DECIMALS = 2

# automatically classify all audio files under this duration as `hits`
AUDIO_DEFAULTS_HIT_IS_DURATION_UNDER_N_SECONDS = 5.0
