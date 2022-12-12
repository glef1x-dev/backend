from django.conf import settings

if settings.DEBUG:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = settings.BASE_DIR / "media"
