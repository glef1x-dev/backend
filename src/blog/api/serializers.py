from typing import Any, Dict

from drf_extra_fields.fields import HybridImageField
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from blog.models import Article
from blog.models import ArticleLike
from blog.models import ArticleTag
from blog.services import create_article
from common.rest_api.deferred import DeferredSerializerMixin


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


class ArticleSerializer(DeferredSerializerMixin, WritableNestedModelSerializer):
    tags = ArticleTagSerializer(many=True)
    image = HybridImageField()
    likes_count = serializers.SerializerMethodField(read_only=True)
    likes = ArticleLikeSerializer(many=True, write_only=True, required=False)
    reading_time_minutes = serializers.FloatField(read_only=True)

    def create(self, validated_data: Dict[str, Any]) -> Article:
        return create_article(**validated_data)

    def get_likes_count(self, article: Article) -> int:
        try:
            return article.likes_count
        except AttributeError:
            return 0

    def get_reading_time_minutes(self, article: Article) -> float:
        return article.reading_time

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
            "reading_time_minutes",
        ]
        ordering = ("-modified", "-created")
        deferred_fields_for_list_serializer = ["body", "description"]
