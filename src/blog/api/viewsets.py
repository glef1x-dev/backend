from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from blog.api.serializers import ArticleSerializer
from blog.models import Article
from common.rest_api.api_view_error_mixin import DeveloperErrorViewMixin


@extend_schema(
    tags=["blog"]
)
class ArticleViewSet(DeveloperErrorViewMixin, ModelViewSet):
    serializer_class = ArticleSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Article.objects.order_by('created').prefetch_related('tags').all()
