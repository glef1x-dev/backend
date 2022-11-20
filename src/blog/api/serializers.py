from drf_extra_fields.fields import HybridImageField
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from blog.models import ArticleTag, Article


class ArticleTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleTag
        fields = '__all__'


class ArticleSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    tags = ArticleTagSerializer(required=False, many=True)
    image = HybridImageField()

    class Meta:
        model = Article
        fields = ["title", "image", "created", "modified", "description", "body", "tags", "slug"]
