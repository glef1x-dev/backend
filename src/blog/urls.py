from rest_framework.routers import DefaultRouter

from django.urls import path

from blog.api.viewsets import ArticleCreateView
from blog.api.viewsets import ArticleReadOnlyViewSet
from blog.api.viewsets import ArticleUpdateView

router = DefaultRouter()

router.register(r"articles", ArticleReadOnlyViewSet, basename="article")

app_name = "blog"

urlpatterns = [
    *router.urls,
    path(r"articles/<slug:slug>/", ArticleUpdateView.as_view(), name="article-update"),
    path(r"articles/", ArticleCreateView.as_view(), name="article-create"),
]
