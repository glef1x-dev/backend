# Create your DRF serializers here
# https://www.django-rest-framework.org/tutorial/1-serialization/#creating-a-serializer-class
from typing import Any, Dict

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer

from django.conf import settings


class TokenBlackListSerializer(TokenBlacklistSerializer):
    refresh = serializers.CharField(required=False)

    def validate(self, attrs: Dict[str, Any]):
        request: Request = self.context["request"]
        refresh_token = attrs.get("refresh") or request.COOKIES.get(
            settings.REFRESH_TOKEN_COOKIE_NAME
        )

        if not refresh_token:
            raise ValidationError(
                {
                    "refresh": "Refresh token value should be passed through data or the cookies"
                }
            )

        refresh = self.token_class(refresh_token)
        try:
            refresh.blacklist()
        except AttributeError:
            pass

        return {}
