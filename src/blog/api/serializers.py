from typing import Any, Dict

from drf_extra_fields.fields import HybridImageField
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from blog.models import Article
from blog.models import ArticleLike
from blog.models import ArticleTag
from blog.services import create_article


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
    likes = ArticleLikeSerializer(many=True, write_only=True, required=False)

    def create(self, validated_data: Dict[str, Any]) -> Article:
        return create_article(**validated_data)

    @property
    def _readable_fields(self):
        for field in self.fields.values():
            if field.write_only:
                continue
            if (
                self.parent
                and field.field_name in self.Meta.deferred_fields_for_list_serializer
            ):
                continue

            yield field

    def get_likes_count(self, article: Article) -> int:
        try:
            return article.likes_count
        except AttributeError:
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
        deferred_fields_for_list_serializer = ["body", "description"]
