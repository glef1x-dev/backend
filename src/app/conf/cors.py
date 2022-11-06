from corsheaders.defaults import default_headers

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers) + ['Content-Range']
CORS_EXPOSE_HEADERS = ['Content-Range']
