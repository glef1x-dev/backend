from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from blog.models import ArticleTag, Article
from drf_extra_fields.fields import Base64ImageField


class ArticleTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleTag
        fields = '__all__'


class ArticleSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    tags = ArticleTagSerializer(required=False, many=True)
    image = Base64ImageField()

    class Meta:
        model = Article
        fields = ["title", "image", "created", "modified", "description", "body", "tags", "slug"]
