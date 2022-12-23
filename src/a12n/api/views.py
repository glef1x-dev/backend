from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

from django.conf import settings

from a12n.utils import delete_refresh_token_cookie
from a12n.utils import set_refresh_token_cookie


@extend_schema(summary="Get a new jwt token pair")
class ObtainJSONWebTokenView(TokenObtainPairView):
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        response = super().post(request, *args, **kwargs)
        set_refresh_token_cookie(response)
        return response


@extend_schema(summary="Refresh a jwt access token")
class RefreshJSONWebTokenView(TokenRefreshView):
    """
    Allows a frontend application to send the refresh token implicitly
    and use the `httpOnly` flag on the refresh token cookie in order to
    avoid potential security problems
    """

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        request.data.setdefault(
            "refresh", request.COOKIES.get(settings.REFRESH_TOKEN_COOKIE_NAME)
        )
        response = super().post(request, *args, **kwargs)
        set_refresh_token_cookie(response)
        return response


@extend_schema(summary="Verify a jwt access token")
class VerifyJSONWebTokenView(TokenVerifyView):
    pass


@extend_schema(summary="Blacklist a token")
class BlacklistJSONWebTokenView(TokenBlacklistView):
    _serializer_class = "a12n.api.serializers.TokenBlackListSerializer"

    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)

        if request.COOKIES.get(settings.REFRESH_TOKEN_COOKIE_NAME):
            delete_refresh_token_cookie(response)

        return response
