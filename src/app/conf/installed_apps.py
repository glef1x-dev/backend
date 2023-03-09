# Application definition

from app.conf.env_reader import env

APPS = ["app", "a12n", "users", "blog", "third_party"]

HEALTH_CHECKS_APPS = [
    "health_check",
    "health_check.db",
]

THIRD_PARTY_APPS = [
    "baton",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "corsheaders",
    "axes",
    "django_prometheus",
    "debug_toolbar",
    "baton.autodiscover",
]

SITE_ID = 1

INSTALLED_APPS = APPS + HEALTH_CHECKS_APPS + THIRD_PARTY_APPS

# In production disable unused apps
if not env("DEBUG", default=True):
    INSTALLED_APPS.remove("baton")
    INSTALLED_APPS.remove("django.contrib.admin")
    INSTALLED_APPS.remove("django.contrib.sessions")
    INSTALLED_APPS.remove("django.contrib.messages")
    INSTALLED_APPS.remove("baton.autodiscover")
    INSTALLED_APPS.remove("debug_toolbar")
