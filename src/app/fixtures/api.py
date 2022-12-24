from datetime import timedelta
import pytest

from pytest_django.plugin import _DatabaseBlocker

from django.conf import settings

from app.testing import ApiClient
from users.tests.factories import UserFactory


def pytest_configure() -> None:
    settings.configure(SIMPLE_JWT={"ACCESS_TOKEN_LIFETIME": timedelta(days=1)})


@pytest.fixture(scope="module")
def as_anon() -> ApiClient:
    return ApiClient()


@pytest.fixture(scope="module")
def as_user(django_db_blocker: _DatabaseBlocker) -> ApiClient:
    api_client = ApiClient()
    # We have to unblock database using django_db_blocker in order to use
    # module scoped fixtures in conjunction with pytest-django
    # https://github.com/pytest-dev/pytest-django/issues/514
    with django_db_blocker.unblock():
        api_client.authorize(UserFactory.create(password="test"))
        yield api_client
