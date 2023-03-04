from typing import Any

from github import Github
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from urllib3 import Retry

from django.conf import settings


class GithubApiView(GenericAPIView):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._github_api_client = Github(
            login_or_token=settings.GITHUB_API_TOKEN, retry=Retry(total=20)
        )

    def get(self, request: Request, repo: str, owner: str) -> Response:
        repository = self._github_api_client.get_repo(f"{owner}/{repo}")
        return Response(
            {
                "stargazers_count": repository.stargazers_count,
                "html_url": repository.html_url,
                "full_name": repository.full_name,
            },
            content_type="application/json",
        )
