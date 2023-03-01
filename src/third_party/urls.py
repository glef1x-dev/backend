from django.urls import path

from third_party.api.viewsets import GithubApiView
from third_party.services import GithubService

app_name = "third_party"
urlpatterns = [
    path(
        "github/repository/<str:owner>/<str:repo>/",
        GithubApiView.as_view(github_service=GithubService()),
        name="github-repo-data",
    ),
]
