from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from common.rest_api.api_view_error_mixin import DeveloperErrorViewMixin
from users.api.serializers import UserSerializer
from users.models import User


@extend_schema(
    summary="Get a current user",
    description="Get a current user using authorization that was provided"
)
class SelfView(DeveloperErrorViewMixin, RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User:
        return self.get_queryset().get(pk=self.request.user.pk)

    def get_queryset(self) -> QuerySet[User]:
        return User.objects.filter(is_active=True)
