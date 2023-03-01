# This file was generated using http://github.com/f213/django starter template.
#
# Settings are split into multiple files using http://github.com/sobolevn/django-split-settings
import warnings

from split_settings.tools import include

from django.core.management.utils import get_random_secret_key

from app.conf.env_reader import env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default=None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", cast=bool, default=True)
CI = env("CI", cast=bool, default=False)

if not SECRET_KEY and DEBUG:
    warnings.warn("SECRET_KEY not configured, using a random temporary key.")
    SECRET_KEY = get_random_secret_key()

include(
    "conf/boilerplate.py",
    "conf/api.py",
    "conf/auth.py",
    "conf/db.py",
    "conf/http.py",
    "conf/i18n.py",
    "conf/installed_apps.py",
    "conf/media.py",
    "conf/middleware.py",
    "conf/storage.py",
    "conf/sentry.py",
    "conf/static.py",
    "conf/templates.py",
    "conf/timezone.py",
    "conf/logs.py",
    "conf/caching.py",
    "conf/third_party.py",
)
