from django.conf import settings

from app.conf.env_reader import env

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_ROOT = env("STATIC_ROOT", cast=str, default="static")

if settings.DEBUG:
    STATIC_URL = "/static/"
else:
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"
