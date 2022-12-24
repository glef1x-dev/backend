import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_401_UNAUTHORIZED

from app.testing import ApiClient
from users.models import User

pytestmark = pytest.mark.django_db


def test_ok(as_user: ApiClient, user: User):
    response = as_user.get(reverse("v1:users:get-current-user"), format="json")

    assert response.data["id"] == user.pk
    assert response.data["username"] == user.username


def test_anon_get_current_user_fails(as_anon: ApiClient):
    as_anon.get(
        reverse("v1:users:get-current-user"), expected_status=HTTP_401_UNAUTHORIZED
    )
