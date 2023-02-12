# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

from app.conf.env_reader import env

DATABASES = {
    "default": env.db_url(
        default="postgres://postgres:postgres@localhost:5432/testdb",
    )
}

# https://docs.djangoproject.com/en/3.2/releases/3.2/#customizing-type-of-auto-created-primary-keys
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
