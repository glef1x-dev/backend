import pytest

from django.apps import apps
from django.conf import LazySettings

from app.testing.api import ApiClient

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def _require_users_app_installed(settings: LazySettings) -> None:
    assert apps.is_installed(
        "users"
    ), """
        Stock f213/django users app should be installed to run this test.

        Make sure to test app.middleware.real_ip.real_ip_middleware on your own, if you drop
        the stock users app.
    """


def test_remote_addr(as_user: ApiClient) -> None:
    result = as_user.get(
        "/api/v1/users/me/", HTTP_X_FORWARDED_FOR="100.200.250.150, 10.0.0.1"
    )

    assert result.data["remote_addr"] == "100.200.250.150"
