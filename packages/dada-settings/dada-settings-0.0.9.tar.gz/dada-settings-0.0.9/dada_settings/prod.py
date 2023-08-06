import os

DEBUG = False
SQLALCHEMY_DATABASE_URI = os.getenv(
    "DADA_SQLALCHEMY_DATABASE_URI_PROD", "postgresql://localhost:5432/dada"
)
# SQLALCHEMY_ECHO = True
S3_BUCKET = os.getenv("DADA_S3_BUCKET_PROD", "dada")
