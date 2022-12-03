import pytest

from rest_framework.reverse import reverse

pytestmark = [pytest.mark.django_db]


def test_ok(as_user, user):
    result = as_user.get(reverse("v1:users:get-current-user"))

    assert result["id"] == user.pk
    assert result["username"] == user.username


def test_anon(as_anon):
    result = as_anon.get(reverse("v1:users:get-current-user"), as_response=True)

    assert result.status_code == 401
