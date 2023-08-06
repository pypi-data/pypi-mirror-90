import os
from dotenv import load_dotenv

load_dotenv()

# app

SECRET_KEY = os.getenv("DADA_SUPER_USER_SECRET_KEY", "dada123")
PORT = os.getenv("DADA_PORT", 3030)
HOST = os.getenv("DADA_HOST", "0.0.0.0")
HTTPS = os.getenv("DADA_HTTPS", "false").lower() == "true"
DEFAULT_BASE_URL = "http://localhost:3030"
if HTTPS:
    DEFAULT_BASE_URL = DEFAULT_BASE_URL.replace("http", "https")
BASE_URL = os.getenv("DADA_BASE_URL", DEFAULT_BASE_URL)
API_VERSION = os.getenv("DADA_API_VERSION", "1.0.0")
API_KEY_HEADER = os.getenv("DADA_API_KEY_HEADER", "X-DADA-API-KEY")
ENV_VAR_PREFIX = os.getenv("DADA_ENV_VAR_PREFIX", "dada")

# db
SQLALCHEMY_DATABASE_URI = os.getenv(
    "DADA_SQLALCHEMY_DATABASE_URI", "postgresql://localhost:5432/dada"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# super user
SUPER_USER_NAME = os.getenv("DADA_SUPER_USER_NAME", "gltd")
SUPER_USER_EMAIL = os.getenv("DADA_SUPER_USER_EMAIL", "dev@globally.ltd")
SUPER_USER_PASSWORD = os.getenv("DADA_SUPER_USER_PASSWORD", "dev")
SUPER_USER_API_KEY = os.getenv("DADA_SUPER_USER_API_KEY", "dev")

# filesearch
FILE_SEARCH_RESULTS_PER_PAGE = os.getenv("DADA_FILE_SEARCH_RESULTS_PER_PAGE", 10)

# celery
CELERY_BROKER_URL = os.getenv("DADA_CELERY_BROKER_URL", "redis://localhost:6379")
CELERY_RESULT_BACKEND = os.getenv(
    "DADA_CELERY_RESULT_BACKEND", "redis://localhost:6379"
)
CELERY_ACCEPT_CONTENT = [os.getenv("DADA_CELERY_ACCEPT_CONTENT", "application/json")]
CELERY_RESULT_SERIALIZER = os.getenv("DADA_CELERY_RESULT_SERIALIZER", "json")
CELERY_TASK_SERIALIZER = os.getenv("DADA_CELERY_TASK_SERIALIZER", "json")

# redis cache
REDIS_CACHE_URL = os.getenv("DADA_REDIS_CACHE_URL", "redis://localhost:6379/")
REDIS_CACHE_DB = os.getenv("DADA_REDIS_CACHE_DB", "0")
REDIS_CACHE_KWARGS = os.getenv("DADA_REDIS_CACHE_KWARGS", {})
REDIS_CACHE_SERIALIZER = "pickle"  # TODO: implement something else?

# email
EMAIL_HOST = os.getenv("DADA_EMAIL_HOST", "mail.gandi.net")
EMAIL_FROM_USER = os.getenv("DADA_EMAIL_FROM_USER", "lola@gltd.cat")
EMAIL_FROM_USER_FULL_NAME = os.getenv("DADA_EMAIL_FROM_USER_FULL_NAME", "lola")
EMAIL_FROM_USER_SMTP_PORT = int(os.getenv("DADA_EMAIL_SMTP_PORT", 587))
EMAIL_FROM_USER_IMAP_PORT = int(os.getenv("DADA_EMAIL_IMAP_PORT", 998))
EMAIL_PASSWORD = os.getenv("DADA_EMAIL_PASSWORD")

# filestore
TEMPFILE_DIR = os.getenv("DADA_TMP_DIR", "/tmp")  # override for docker environment
LOCAL_DIR = os.getenv("DADA_LOCAL_DIR", os.path.expanduser("~/.dada/stor/"))
S3_PLATFORM = os.getenv("DADA_S3_PLATFORM", "do")
if S3_PLATFORM == "do":
    S3_HOST = "digitaloceanspaces.com"
else:
    S3_HOST = "s3.amazonaws.com"  # TODO: check this.

S3_BUCKET = os.getenv("DADA_S3_BUCKET", "dada.globally.ltd")
S3_ACCESS_KEY_ID = os.getenv("DADA_S3_ACCESS_KEY_ID")
S3_SECRET_ACCESS_KEY = os.getenv("DADA_S3_SECRET_ACCESS_KEY")
S3_REGION_NAME = os.getenv("DADA_S3_REGION_NAME", "nyc3")
S3_BASE_URL = os.getenv(
    "DADA_S3_BASE_URL", f"https://{S3_BUCKET}.{S3_REGION_NAME}.{S3_HOST}"
)
S3_ENDPOINT_URL = os.getenv(
    "DADA_S3_ENDPOINT_URL", f"https://{S3_REGION_NAME}.{S3_HOST}"
)

# api spec
APISPEC_SWAGGER_URL = os.getenv("DADA_APISPEC_SWAGGER_URL", "/spec/")
APISPEC_SWAGGER_UI_URL = os.getenv("DADA_APISPEC_SWAGGER_UI_URL", "/docs/")

# logging settings
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {"format": ("<%(levelname)s> %(message)s [%(asctime)s]")}
    },
    "datefmt": "%I:%M:%S",
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

LOG_LEVEL = os.getenv("DADA_LOG_LEVEL", "debug")
