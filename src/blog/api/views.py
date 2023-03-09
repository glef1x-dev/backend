from typing import Any, List

from django_filters import filters
from django_filters import FilterSet
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Count
from django.db.models import QuerySet

from blog.api.serializers import ArticleSerializer
from blog.models import Article
from blog.models import ArticleTag
from blog.utils.cache import compose_cache_key
from blog.utils.cache import iter_all_possible_cache_keys_to_invalidate
from common.images import convert_image_to_webp_format
from common.rest_api.api_view_error_mixin import DeveloperErrorViewMixin


class ArticleFilter(FilterSet):
    has_tag = filters.CharFilter("tags__title", lookup_expr="iexact")

    class Meta:
        model = Article
        fields = ["tags__title"]


class ArticleCursorPagination(CursorPagination):
    page_size = 10
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

    def list(self, request, *args, **kwargs) -> Response:
        # TODO: maybe I should make more generic caching and don't be so bounded to specifics
        if request.query_params.get(
            self.pagination_class.page_size_query_param
        ) or request.query_params.get(self.pagination_class.cursor_query_param):
            return super().list(request, *args, **kwargs)

        cache_key = compose_cache_key(
            "articles",
            request.query_params.get("tags__title"),
        )
        if not (articles := cache.get(cache_key)):
            response = super().list(request, *args, **kwargs)
            cache.set(cache_key, response.data, settings.DEFAULT_CACHE_TIME)
            return response

        return Response(articles)

    def perform_update(self, serializer: ArticleSerializer) -> None:
        super().perform_update(serializer)
        tags: List[ArticleTag] = serializer.data.tags
        cache.delete_many([*iter_all_possible_cache_keys_to_invalidate(tags=tags)])

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        cache_key = compose_cache_key("article", self.kwargs[self.lookup_field])
        if not (article := cache.get(cache_key)):
            article = self.get_object()
            cache.set(cache_key, article, settings.DEFAULT_CACHE_TIME)

        serializer = self.get_serializer(article)
        return Response(serializer.data)

    def get_queryset(self) -> QuerySet[Article]:
        article_queryset = (
            Article.objects.prefetch_related("tags")
            .order_by("-created")
            .annotate(likes_count=Count("likes__id"))
        )

        if self.request.method == "GET" and not self.detail:
            article_queryset = article_queryset.defer("body", "description")

        return article_queryset
