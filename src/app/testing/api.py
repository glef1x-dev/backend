from rest_framework.response import Response
from rest_framework.test import APIClient as DRFAPIClient
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User


class ApiClient(DRFAPIClient):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def authorize(self, user: User) -> "ApiClient":
        access_token = AccessToken.for_user(user)
        self.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        return self

    def get(self, *args, **kwargs):
        expected_status = kwargs.get("expected_status", 200)
        return self._request("get", expected_status, *args, **kwargs)

    def patch(self, *args, **kwargs):
        expected_status = kwargs.get("expected_status", 200)
        return self._request("patch", expected_status, *args, **kwargs)

    def post(self, *args, **kwargs):
        expected_status = kwargs.get("expected_status", 201)
        return self._request("post", expected_status, *args, **kwargs)

    def put(self, *args, **kwargs):
        expected_status = kwargs.get("expected_status", 200)
        return self._request("put", expected_status, *args, **kwargs)

    def delete(self, *args, **kwargs):
        expected_status = kwargs.get("expected_status", 204)
        return self._request("delete", expected_status, *args, **kwargs)

    def _request(self, method, expected, *args, **kwargs) -> Response:
        kwargs["format"] = kwargs.get("format", "json")
        method = getattr(super(), method)

        response: Response = method(*args, **kwargs)
        assert response.status_code == expected
        return response

    @staticmethod
    def is_json(response) -> bool:
        if response.has_header("content-type"):
            return "json" in response.get("content-type")

        return False


__all__ = [
    "ApiClient",
]
