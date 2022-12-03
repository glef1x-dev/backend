from django.db.models import QuerySet, Count
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from blog.api.serializers import ArticleSerializer
from blog.models import Article
from common.rest_api.api_view_error_mixin import DeveloperErrorViewMixin


@extend_schema(
    tags=["blog"]
)
class ArticleCreateView(DeveloperErrorViewMixin, generics.CreateAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=["blog"]
)
class ArticleUpdateView(DeveloperErrorViewMixin, generics.UpdateAPIView):
    serializer_class = ArticleSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=["blog"]
)
class ArticleReadOnlyViewSet(DeveloperErrorViewMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

    def get_queryset(self) -> QuerySet[Article]:
        article_queryset = Article.objects.order_by('created').prefetch_related('tags')

        return article_queryset.annotate(
            likes_count=Count('likes__id')
        )
