from rest_framework import serializers

from blog.models import ArticleTag, Article


class ArticleTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleTag
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    tags = ArticleTagSerializer(many=True)

    class Meta:
        model = Article
        fields = '__all__'
