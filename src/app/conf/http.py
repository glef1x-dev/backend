from app.conf.env_reader import env

ALLOWED_HOSTS = ['*']  # host validation is not necessary in 2020
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8080',
]

if env('DEBUG'):
    ABSOLUTE_HOST = 'http://localhost:3000'
else:
    ABSOLUTE_HOST = 'https://your.app.com'

APPEND_SLASH = False
