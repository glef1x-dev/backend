from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
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


class DeleteRetrieveUpdateArticleViewSet(DeveloperErrorViewMixin, ModelViewSet):
    serializer_class = ArticleSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Article]:
        return Article.objects.filter(slug=self.kwargs['slug'])

    def check_permissions(self, request: Request):
        if request.method == "GET":
            return

        super().check_permissions(request)

