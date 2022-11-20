from django.urls import path, include
from rest_framework.routers import DefaultRouter

from blog.api.viewsets import ArticleViewSet

router = DefaultRouter()

router.register(r'articles', ArticleViewSet, basename='article')

app_name = 'blog'

urlpatterns = [
    path(r'blog/', include(router.urls))
]
