from django_filters import filters
from django_filters import FilterSet
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Count
from django.db.models import QuerySet

from blog.api.serializers import ArticleSerializer
from blog.models import Article
from common.images import convert_image_to_webp_format
from common.rest_api.api_view_error_mixin import DeveloperErrorViewMixin


class ArticleFilter(FilterSet):
    has_tag = filters.CharFilter("tags__title", lookup_expr="iexact")

    class Meta:
        model = Article
        fields = ["tags__title"]


class ArticleCursorPagination(CursorPagination):
    page_size = 4  # Should be a multiple of 2
    page_size_query_param = "page_size"


@extend_schema(tags=["blog"])
class ArticleViewSet(DeveloperErrorViewMixin, viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    lookup_field = "slug"
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = ArticleFilter
    pagination_class = ArticleCursorPagination

    def perform_create(self, serializer: ArticleSerializer) -> None:
        article_image: SimpleUploadedFile = serializer.validated_data.get("image")
        convert_image_to_webp_format(article_image)
        serializer.save()

    def list(self, request, *args, **kwargs):
        if not (articles := cache.get("articles")):
            response = super().list(request, *args, **kwargs)
            cache.set("articles", response.data, settings.DEFAULT_CACHE_TIME)
            return response

        return Response(articles)

    def perform_update(self, serializer) -> None:
        super().perform_update(serializer)
        cache.delete("articles")

    def get_queryset(self) -> QuerySet[Article]:
        article_queryset = (
            Article.objects.prefetch_related("tags")
            .order_by("-created")
            .annotate(likes_count=Count("likes__id"))
        )

        return article_queryset
