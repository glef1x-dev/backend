from http.cookies import SimpleCookie
import pytest

from pytest_django.plugin import _DatabaseBlocker
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_401_UNAUTHORIZED

from app.testing import ApiClient
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def _disable_django_axes(settings):
    settings.AXES_ENABLED = False


@pytest.fixture(scope="module")
def token_pair(as_anon: ApiClient, django_db_blocker: _DatabaseBlocker):
    # We have to unblock database using django_db_blocker in order to use
    # module scoped fixtures in conjunction with pytest-django
    # https://github.com/pytest-dev/pytest-django/issues/514
    with django_db_blocker.unblock():
        dummy_user = UserFactory.create(password="test")
        response = as_anon.post(
            reverse("v1:a12n:obtain-token"),
            {
                "username": dummy_user.username,
                "password": "test",
            },
            format="json",
            expected_status=HTTP_200_OK,
        )
        assert response.cookies.get("refresh").value is not None
        yield response.data


def test_refresh_token(as_anon: ApiClient, token_pair: dict[str, str]):
    response = as_anon.post(
        reverse("v1:a12n:refresh-token"),
        {"refresh": token_pair["refresh"]},
        format="json",
        expected_status=HTTP_200_OK,
    )

    assert response.data["access"] != token_pair["access"]
    assert response.cookies["refresh"].value == response.data["refresh"]


def test_verify_token(as_anon: ApiClient, token_pair: dict[str, str]):
    as_anon.post(
        reverse("v1:a12n:verify-token"),
        {"token": token_pair["access"]},
        format="json",
        expected_status=HTTP_200_OK,
    )


@pytest.mark.parametrize(
    "wrong_token",
    [
        "string",
        "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY1NjA3ODYzLCJpYXQiOjE2NjU2MDc4MDMsImp0aSI6IjZhN2M4OWM5MmNlYjRkZjBhNTdhMTllYzBiMzk3YTQ2IiwidXNlcl9pZCI6Mn0.2goxBUKxQUfLSN3h6AausIsuSWblY2N63H3kmZhvy9naS8htP6NPFpv1ZDWPNo7Ddl8TeMq8JYCkl_Wt4w-zSA ",
    ],
)
def test_verify_token_failure(as_anon: ApiClient, wrong_token: str):
    as_anon.post(
        reverse("v1:a12n:verify-token"),
        {"token": "bla-bla-bla"},
        format="json",
        expected_status=HTTP_401_UNAUTHORIZED,
    )


def test_blacklist_refresh_token(as_user: ApiClient, token_pair: dict[str, str]):
    response = as_user.post(
        reverse("v1:a12n:blacklist-token"),
        {"refresh": token_pair["refresh"]},
        format="json",
        expected_status=HTTP_200_OK,
    )
    with pytest.raises(KeyError):
        # The cookie was deleted after blacklisting
        _ = response.cookies["refresh"]

    as_user.post(
        reverse("v1:a12n:refresh-token"),
        {"refresh": token_pair["refresh"]},
        format="json",
        expected_status=HTTP_401_UNAUTHORIZED,
    )


def test_fail_blacklist_non_existent_refresh_token(as_user: ApiClient):
    as_user.post(
        reverse("v1:a12n:blacklist-token"),
        {"refresh": "aaa"},
        format="json",
        expected_status=HTTP_401_UNAUTHORIZED,
    )


def test_blacklist_refresh_token_through_cookie(
    as_user: ApiClient, token_pair: dict[str, str]
):
    as_user.cookies = SimpleCookie({"refresh": token_pair["refresh"]})

    as_user.post(
        reverse("v1:a12n:blacklist-token"),
        format="json",
        expected_status=HTTP_200_OK,
    )

    as_user.post(
        reverse("v1:a12n:refresh-token"),
        {"refresh": token_pair["refresh"]},
        format="json",
        expected_status=HTTP_401_UNAUTHORIZED,
    )
