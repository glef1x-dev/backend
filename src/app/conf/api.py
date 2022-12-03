from app.conf.env_reader import env

# Django REST Framework
# https://www.django-rest-framework.org/api-guide/settings/

DISABLE_THROTTLING = env("DISABLE_THROTTLING", cast=bool, default=False)
MAX_PAGE_SIZE = env("MAX_PAGE_SIZE", cast=int, default=1000)

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "common.rest_api.exception_handler.custom_exception_handler",
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "app.api.renderers.AppJSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
    ],
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "DEFAULT_PAGINATION_CLASS": "app.api.pagination.AppPagination",
    "PAGE_SIZE": env("PAGE_SIZE", cast=int, default=20),
    "DEFAULT_THROTTLE_RATES": {
        "anon-auth": "30/min",
    },
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# Set up drf_spectacular, https://drf-spectacular.readthedocs.io/en/latest/settings.html
SPECTACULAR_SETTINGS = {
    "TITLE": "Admin auth/data provider",
    "DESCRIPTION": "Serves as a provider for admin panel",
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "VERSION": "1.0.0",
    "REDOC_DIST": "SIDECAR",
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.hooks.postprocess_schema_enums",
        "drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields",
    ],
    "CONTACT": {"name": "Hlib", "email": "glebgar567@gmail.com"},
}
