from rest_framework.status import HTTP_200_OK

from django.urls import reverse

from app.testing import ApiClient


def test_get_stargazers_count_by_repo_name(as_anon: ApiClient):
    response = as_anon.get(
        reverse(
            "v1:third_party:github-repo-data",
            kwargs={"repo": "hello-world", "owner": "Fetcher32"},
        ),
        format="json",
        expected_status=HTTP_200_OK,
    )

    assert response.data["stargazers_count"] >= 0
