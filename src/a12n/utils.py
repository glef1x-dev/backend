from rest_framework.response import Response
from rest_framework_simplejwt.settings import api_settings

from django.conf import settings


def set_refresh_token_cookie_to_admin_panel(response: Response) -> Response:
    refresh_token = response.data['refresh']
    response.set_cookie(
        settings.REFRESH_TOKEN_COOKIE_NAME,
        refresh_token,
        max_age=api_settings.REFRESH_TOKEN_LIFETIME,
        httponly=True,
        samesite="Strict",
        domain=f"https://admin.{settings.ROOT_DOMAIN}"
    )
    return response
