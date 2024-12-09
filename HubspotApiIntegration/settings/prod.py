import dj_database_url

DEBUG = False

ALLOWED_HOSTS=["https://restapi-yzh1.onrender.com","localhost"]


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

