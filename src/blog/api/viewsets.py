from django.db.models import QuerySet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from blog.api.serializers import ArticleSerializer
from blog.models import Article
from common.rest_api.api_view_error_mixin import DeveloperErrorViewMixin


@extend_schema(
    tags=["blog"]
)
class CreateListArticlesAPIViewSet(DeveloperErrorViewMixin, ModelViewSet):
    queryset = Article.objects.order_by('created').prefetch_related('tags').all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class RetrieveArticleBySlug(DeveloperErrorViewMixin, RetrieveAPIView):
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

    def get_queryset(self) -> QuerySet[Article]:
        return Article.objects.filter(slug=self.kwargs['slug'])


@extend_schema(
    parameters=[
        OpenApiParameter("slug", OpenApiTypes.STR),
    ],
    description="Deletes blog post by it's id or slug",
    summary="Deletes blog post",
    tags=["blog"]
)
class DeleteArticleAPIView(DeveloperErrorViewMixin, DestroyAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ("slug",)


class UpdateArticleAPIView(DeveloperErrorViewMixin, UpdateAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Article.objects.filter(pk=self.kwargs['pk'])
