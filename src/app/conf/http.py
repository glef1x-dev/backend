from app.conf.env_reader import env

ALLOWED_HOSTS = ['*']  # host validation is not necessary in 2020

if env('DEBUG'):
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:8000"
    ]
    ABSOLUTE_HOST = 'http://localhost:8000'
else:
    APP_URL = env.str("APP_URL")
    ABSOLUTE_HOST = APP_URL
    CSRF_TRUSTED_ORIGINS = [
        APP_URL
    ]

APPEND_SLASH = False
