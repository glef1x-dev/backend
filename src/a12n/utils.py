from rest_framework.response import Response
from rest_framework_simplejwt.settings import api_settings

from django.conf import settings

_BASE_COOKIES_PARAMS = {
    "key": settings.REFRESH_TOKEN_COOKIE_NAME,
    "path": "/",
    "samesite": "Lax",
}


def set_refresh_token_cookie(response: Response) -> Response:
    refresh_token = response.data["refresh"]
    set_cookie_params = _BASE_COOKIES_PARAMS | {
        "value": refresh_token,
        "max_age": api_settings.REFRESH_TOKEN_LIFETIME,
        "httponly": True,
        "secure": True,
    }
    response.set_cookie(**set_cookie_params)
    return response


def delete_refresh_token_cookie(response: Response) -> None:
    response.delete_cookie(**_BASE_COOKIES_PARAMS)
