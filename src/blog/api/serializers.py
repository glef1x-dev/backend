from typing import Dict, Any

from django.db import transaction
from drf_extra_fields.fields import HybridImageField
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from blog.models import ArticleTag, Article
from blog.services import create_article_from_dictionary


class ArticleTagSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    """Defining title as a field prevents the unique validation using the title field"""

    class Meta:
        model = ArticleTag
        fields = ('title', 'id')
        ordering = ('-id',)


class ArticleSerializer(WritableNestedModelSerializer):
    tags = ArticleTagSerializer(many=True)
    image = HybridImageField()

    @transaction.atomic
    def create(self, validated_data: Dict[str, Any]) -> Article:
        return create_article_from_dictionary(validated_data)

    class Meta:
        model = Article
        fields = ["title", "created", "image", "modified", "description", "body", "tags", "slug"]
        ordering = ('-modified',)
