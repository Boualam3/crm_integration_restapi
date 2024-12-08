
import dj_database_url


DATABASES = {
    'default': dj_database_url.config(
        default="postgresql://postgres:postgres@localhost:5432/API_DB",        conn_max_age=600)
}
