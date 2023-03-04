from django.urls import path

from third_party.api.viewsets import GithubApiView

app_name = "third_party"
urlpatterns = [
    path(
        "github/repository/<str:owner>/<str:repo>/",
        GithubApiView.as_view(),
        name="github-repo-data",
    ),
]
