from datetime import timedelta
import pytest

from django.conf import settings

from app.testing import ApiClient
from users.models import User


def pytest_configure() -> None:
    settings.configure(SIMPLE_JWT={"ACCESS_TOKEN_LIFETIME": timedelta(days=1)})


@pytest.fixture
def as_anon() -> ApiClient:
    return ApiClient()


@pytest.fixture
def as_user(user: User) -> ApiClient:
    api_client = ApiClient()
    api_client.authorize(user)
    return api_client
