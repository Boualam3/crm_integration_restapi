from .base import *
import dj_database_url
from dotenv import load_dotenv
load_dotenv()
import os

DEBUG = False

ALLOWED_HOSTS=[os.environ.get("ALLOWED_HOST")]


INSTALLED_APPS += ['corsheaders']

MIDDLEWARE += [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173'
]

CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
]



DATABASES = {
    'default': dj_database_url.config(
        default="postgresql://postgres:postgres@localhost:5432/api_db",        conn_max_age=600)
}


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
# and renames the files with unique names for each version to support long-term caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'