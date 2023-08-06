import os

DEBUG = False
SQLALCHEMY_DATABASE_URI = os.getenv(
    "DADA_SQLALCHEMY_DATABASE_URI_DOCKER",
    "postgresql://postgres:secret@postgres:5432/dada",
)
CELERY_BROKER_URL = os.getenv("DADA_CELERY_BROKER_URL_DOCKER", "redis://redis:6379")
CELERY_RESULT_BACKEND = os.getenv(
    "DADA_CELERY_RESULT_BACKEND_DOCKER", "redis://redis:6379"
)

# redis cache
REDIS_CACHE_URL = os.getenv("DADA_REDIS_CACHE_URL", "redis://redis:6379/")
REDIS_CACHE_DB = os.getenv("DADA_REDIS_CACHE_DB", "1")
