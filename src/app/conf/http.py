import urllib.parse

from corsheaders.defaults import default_headers

from app.conf.env_reader import env

ALLOWED_HOSTS = ["*"]  # host validation is not necessary in 2022

if env("DEBUG"):
    CSRF_TRUSTED_ORIGINS = ["http://localhost:8000"]
    ABSOLUTE_HOST = "http://localhost:8000"
    CORS_ALLOW_ALL_ORIGINS = True
else:
    APP_URL = env.str("APP_URL")
    ABSOLUTE_HOST = APP_URL
    CSRF_TRUSTED_ORIGINS = [APP_URL]

    # TODO still unsafe parsing, but I don't wanna install another third-party library
    # Just leave it here if the problem will appear in future for domains like "something.co.uk"
    # https://stackoverflow.com/questions/1521592/get-root-domain-of-link
    root_domain = str(urllib.parse.urlparse(APP_URL).hostname)
    CORS_ALLOWED_ORIGINS = [f"https://{root_domain}", f"https://admin.{root_domain}"]
    CSRF_TRUSTED_ORIGINS = [
        f"https://*.{root_domain}",
    ]

APPEND_SLASH = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers) + ["Content-Range"]
CORS_EXPOSE_HEADERS = ["Content-Range"]
