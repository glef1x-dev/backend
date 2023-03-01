from typing import Any

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from third_party.services import GithubService


class GithubApiView(GenericAPIView):
    github_service: GithubService = None

    def __init__(self, github_service: GithubService, **kwargs: Any):
        super().__init__(**kwargs)
        self.github_service = github_service

    def get(self, request: Request, repo: str, owner: str) -> Response:
        repository = self.github_service.get_repository(repo, owner)
        return Response(
            {
                "stargazers_count": repository.stargazers_count,
                "html_url": repository.html_url,
                "full_name": repository.full_name,
            },
            content_type="application/json",
        )
