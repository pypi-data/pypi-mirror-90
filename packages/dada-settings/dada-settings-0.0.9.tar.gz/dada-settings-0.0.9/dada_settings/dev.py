import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = os.getenv(
    "DADA_SQLALCHEMY_DATABASE_URI_DEV", "postgresql://localhost:5432/dada_dev"
)
SQLALCHEMY_ECHO = os.getenv("DADA_SQLALCHEMY_ECHO", "false") == "true"
CELERY_ALWAYS_EAGER = os.getenv("DADA_CELERY_ALWAYS_EAGER", "true") == "true"
S3_BUCKET = os.getenv("DADA_S3_BUCKET_DEV", "dev.dada.globally.ltd")
