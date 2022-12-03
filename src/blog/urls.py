from django.urls import path
from rest_framework.routers import DefaultRouter

from blog.api.viewsets import ArticleReadOnlyViewSet, ArticleUpdateView, ArticleCreateView

router = DefaultRouter()

router.register(r'articles', ArticleReadOnlyViewSet, basename='article')

app_name = 'blog'

urlpatterns = [
    *router.urls,
    path(r'articles/<slug:slug>/', ArticleUpdateView.as_view(), name='article-update'),
    path(r'articles/', ArticleCreateView.as_view(), name='article-create')
]
