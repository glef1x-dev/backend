from django.conf import settings

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "app.middleware.real_ip.real_ip_middleware",
    "axes.middleware.AxesMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django_structlog.middlewares.RequestMiddleware",
]

if not settings.DEBUG:
    MIDDLEWARE.remove("django.contrib.sessions.middleware.SessionMiddleware")
    MIDDLEWARE.remove("django.contrib.auth.middleware.AuthenticationMiddleware")
    MIDDLEWARE.remove("django.contrib.messages.middleware.MessageMiddleware")
