from corsheaders.defaults import default_headers
import tldextract

from django.conf import settings

from app.conf.env_reader import env

ALLOWED_HOSTS = ["*"]  # host validation is not necessary in 2022

if env("DEBUG"):
    CSRF_TRUSTED_ORIGINS = ["http://localhost:8000"]
    APP_URL = "http://localhost:8000"
    CORS_ALLOW_ALL_ORIGINS = True
    ROOT_DOMAIN = "localhost"  # dummy value
else:
    APP_URL = env.str("APP_URL")
    ROOT_DOMAIN = tldextract.extract(APP_URL).registered_domain
    CORS_ALLOWED_ORIGINS = [f"https://{ROOT_DOMAIN}", f"https://admin.{ROOT_DOMAIN}"]
    CSRF_TRUSTED_ORIGINS = [
        f"https://*.{ROOT_DOMAIN}",
    ]

APPEND_SLASH = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers) + ["Content-Range"]
CORS_EXPOSE_HEADERS = ["Content-Range"]

if not settings.DEBUG:
    # settings for django.middleware.security.SecurityMiddleware
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
