from dataclasses import dataclass

from github import Github
from github.Repository import Repository
from urllib3 import Retry

from django.conf import settings


@dataclass
class GithubService:
    _api_client = Github(
        login_or_token=settings.GITHUB_API_TOKEN, retry=Retry(total=20)
    )

    def get_repository(self, repository_name: str, owner: str) -> Repository:
        return self._api_client.get_repo(f"{owner}/{repository_name}")
