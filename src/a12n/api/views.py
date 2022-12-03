from typing import Any

from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView


@extend_schema(
    summary="Get a new jwt token pair"
)
class ObtainJSONWebTokenView(TokenObtainPairView):
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        response = super().post(request, *args, **kwargs)
        # TODO refactor and move it to the utility function
        refresh_token = response.data['refresh']
        response.set_cookie(
            settings.REFRESH_TOKEN_COOKIE_NAME,
            refresh_token,
            max_age=api_settings.REFRESH_TOKEN_LIFETIME,
            httponly=True,
            samesite='Strict'
        )
        return response


@extend_schema(
    summary="Refresh a jwt access token"
)
class RefreshJSONWebTokenView(TokenRefreshView):
    """
    Allows a frontend application to send the refresh token implicitly
    and use the `httpOnly` flag on the refresh token cookie in order to
    avoid potential security problems
    """

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        request.data.setdefault('refresh', request.COOKIES.get(settings.REFRESH_TOKEN_COOKIE_NAME))
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data['refresh']
        response.set_cookie(
            settings.REFRESH_TOKEN_COOKIE_NAME,
            refresh_token,
            max_age=api_settings.REFRESH_TOKEN_LIFETIME,
            httponly=True,
            samesite='Strict'
        )
        return response


@extend_schema(
    summary="Verify a jwt access token"
)
class VerifyJSONWebTokenView(TokenVerifyView):
    pass


@extend_schema(
    summary="Blacklist a token"
)
class BlacklistJSONWebTokenView(TokenBlacklistView):
    pass
