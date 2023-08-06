import os

SQLALCHEMY_DATABASE_URI = os.getenv(
    "DADA_SQLALCHEMY_DATABASE_URI_TEST", "postgresql://localhost:5432/dada_test"
)
CELERY_ALWAYS_EAGER = True
S3_BUCKET = os.getenv("DADA_S3_BUCKET_TEST", "test.dada.globally.ltd")
