from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView


@extend_schema(
    summary="Get a new jwt token pair"
)
class ObtainJSONWebTokenView(TokenObtainPairView):
    pass


@extend_schema(
    summary="Refresh a jwt access token"
)
class RefreshJSONWebTokenView(TokenRefreshView):
    pass


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
