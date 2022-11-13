from django.conf import settings

from app.conf.env_reader import env

if settings.DEBUG:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = env('MEDIA_ROOT', cast=str, default='media')
