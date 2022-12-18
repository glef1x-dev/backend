from django_filters import filters
from django_filters import FilterSet
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Count
from django.db.models import QuerySet

from blog.api.serializers import ArticleSerializer
from blog.models import Article
from common.images import convert_image_to_webp_format
from common.rest_api.api_view_error_mixin import DeveloperErrorViewMixin


class ArticleFilter(FilterSet):
    has_tag = filters.CharFilter('tags__title', lookup_expr='iexact')

    class Meta:
        model = Article
        fields = ['tags__title']


@extend_schema(tags=["blog"])
class ArticleViewSet(DeveloperErrorViewMixin, viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    lookup_field = "slug"
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = ArticleFilter

    def perform_create(self, serializer: ArticleSerializer) -> None:
        article_image: SimpleUploadedFile = serializer.validated_data.get('image')
        convert_image_to_webp_format(article_image)
        serializer.save()

    def get_queryset(self) -> QuerySet[Article]:
        article_queryset = Article.objects.order_by("created").prefetch_related("tags").annotate(
            likes_count=Count("likes__id")
        )

        return article_queryset
