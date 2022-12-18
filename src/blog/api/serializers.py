import logging
from typing import Any, Dict

from drf_extra_fields.fields import HybridImageField
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from blog.models import Article
from blog.models import ArticleLike
from blog.models import ArticleTag
from blog.services import create_article

logger = logging.getLogger(__name__)


class ArticleTagSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    """Defining title as a field prevents the unique validation using the title field"""

    class Meta:
        model = ArticleTag
        fields = ("title", "id")
        ordering = ("-id",)


class ArticleLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleLike
        fields = ("ip_address", "browser_fingerprint")


class ArticleSerializer(WritableNestedModelSerializer):
    tags = ArticleTagSerializer(many=True)
    image = HybridImageField()
    likes_count = serializers.SerializerMethodField(read_only=True)
    likes = ArticleLikeSerializer(many=True, write_only=True)

    def create(self, validated_data: Dict[str, Any]) -> Article:
        return create_article(**validated_data)

    def get_likes_count(self, article: Article) -> int:
        try:
            return article.likes_count
        except AttributeError:
            logger.error(
                "Likes count field is not set on object required by `ArticleSerializer`."
                "Set default value for likes count = 0.",
                stacklevel=2,
            )
            return 0

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "likes",
            "created",
            "image",
            "modified",
            "description",
            "likes_count",
            "body",
            "tags",
            "slug",
        ]
        ordering = ("-modified",)
