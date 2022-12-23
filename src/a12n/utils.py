import functools
from typing import Any

from rest_framework.response import Response
from rest_framework_simplejwt.settings import api_settings

from django.conf import settings


def set_refresh_token_cookie(response: Response) -> Response:
    refresh_token = response.data["refresh"]
    set_cookie_params = _get_base_cookie_params() | {
        "value": refresh_token,
        "max_age": api_settings.REFRESH_TOKEN_LIFETIME,
        "httponly": True,
        "secure": True,
    }
    response.set_cookie(**set_cookie_params)
    return response


def delete_refresh_token_cookie(response: Response) -> None:
    response.delete_cookie(**_get_base_cookie_params())


@functools.lru_cache
def _get_base_cookie_params() -> dict[str, Any]:
    base_cookie_params = {
        "key": settings.REFRESH_TOKEN_COOKIE_NAME,
        "samesite": "Strict",
        "path": "/",
    }

    if settings.DEBUG:
        return base_cookie_params

    base_cookie_params.update(
        domain=f"https://admin.{settings.ROOT_DOMAIN}",
    )
    return base_cookie_params
