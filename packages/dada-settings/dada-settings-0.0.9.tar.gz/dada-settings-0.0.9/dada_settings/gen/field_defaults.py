# ///////////////////////////////////////
# RANDOM GENERATION
# ///////////////////////////////////////


FIELD_DEFAULTS_RANDOM_GENRE_WORD_1 = [
    "jazz",
    "fizz",
    "hip",
    "yacht",
    "future",
    "cat",
    "dog",
    "ambient" "brunch",
    "twee",
    "future",
    "techno",
    "psych",
    "hypno",
    "anarcho",
    "marxist",
    "wavey",
    "vibey",
    "leftfield",
    "outsider",
    "alt",
    "alternative",
    "eclectic",
    "business",
    "serious",
    "contemporary",
]

FIELD_DEFAULTS_RANDOM_GENRE_WORD_2 = [
    "house",
    "disco",
    "hop",
    "trip",
    "bass",
    "ambient",
    "rock",
    "fusion",
    "funk",
    "dm",
    "music",
    "vibe",
    "wave",
    "drill",
    "trap",
    "boogie",
    "tech",
    "matic",
    "step",
]

FIELD_DEFAULTS_RANDOM_ARTIST_NAME_WORD_1 = [
    "dj",
    "mc",
    "kool dj",
    "ancient",
    "samurai",
    "her majesty",
    "The",
    "fresh",
    "kool mo",
    "jazzy",
    "amadeus",
    "karl",
    "jon",
    "sally",
    "olga",
    "bell",
    "toni",
    "M",
    "J",
    "LL",
    "BB",
    "CC",
    "ZZ",
    "No",
    "Yes",
]


FIELD_DEFAULTS_RANDOM_ALBUM_NAME_WORD_1 = [
    "The",
    "A",
    "One",
    "My",
    "Your",
    "His",
    "Her",
    "Their",
    "Our",
    "It's",
]

FIELD_DEFAULTS_RANDOM_ALBUM_NAME_WORD_2 = [
    "city",
    "county",
    "village",
    "town",
    "place",
    "mountain",
    "club",
    "commune",
    "squire",
    "chapel",
    "dancefloor",
    "disco",
    "valley",
    "isthmus",
    "port",
]
FIELD_DEFAULTS_RANDOM_ALBUM_NAME_WORD_3 = [
    "called",
    "for",
    "against",
    "enraged with",
    "named",
    "known as",
    "they called",
    "she called",
    "he called",
    "that unified in",
    "that fell apart because of",
    "enshrouded in",
    "coverer in",
    "awash in",
]
FIELD_DEFAULTS_RANDOM_ALBUM_NAME_WORD_4 = [
    "justice",
    "loathing",
    "solitude",
    "groove",
    "funk",
    "revolution",
    "retribution",
    "disobedience",
    "anger",
    "pride",
    "lust",
    "envy",
    "sin",
    "greed",
    "love",
    "emotions",
    "feelings",
    "tempers",
]
FIELD_DEFAULTS_RANDOM_ALBUM_NAME_WORD_5 = [
    "EP",
    "LP",
    "12'",
    "7'",
    "2x LP",
    "3x LP",
    "10x LP",
    "Reissue",
    "Greatest Hits",
]

# FIELD_DEFAULTS_RANDOM_TEXT_PATH = path.get_env(
#     "DADA_FIELD_DEFAULTS_RANDOM_TEXT_PATH",
#     path.here(__file__, "assets/raw/txt/mobydick.txt"),
# )
FIELD_DEFAULTS_RANDOM_TEXT = (
    "foo bar baz uqbar dada  dsjafhkasdjhflaskj.dhfakl wuejfilauekjsbfdkl uajsbfklajebsrflk auabejwslkf jbaeslkedfdfjsb alkweejkasfdb lkasejdhbbdfslk uwaesvbdflkuajehsbdf lkjasbdhv fklasfmas "
    * 100
)
# with open(FIELD_DEFAULTS_RANDOM_TEXT_PATH, "r") as f:
#     FIELD_DEFAULTS_RANDOM_TEXT += text.rm_whitespace(f.read())
FIELD_DEFAULTS_RANDOM_TEXT_LENGTH = len(FIELD_DEFAULTS_RANDOM_TEXT)
