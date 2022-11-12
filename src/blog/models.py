from django.contrib.postgres.indexes import HashIndex
from django.db import models
from django_extensions.db.fields import AutoSlugField

from app.models import TimestampedModel, DefaultModel


class Article(TimestampedModel):
    title = models.CharField(max_length=120, verbose_name='Title of the article', db_index=True)
    description = models.CharField(
        verbose_name='Description of the article',
        null=False,
        max_length=300
    )
    body = models.TextField(default='hello world', verbose_name='Article content')
    image = models.ImageField(verbose_name='image of the post', null=True, blank=True)
    tags = models.ManyToManyField('ArticleTag', through='ArticleTagItem')
    slug = AutoSlugField(null=False, blank=False, populate_from="title")

    class Meta:
        verbose_name_plural = 'Articles'
        verbose_name = 'Article'
        indexes = [
            HashIndex(fields=["slug"])
        ]


class ArticleTag(DefaultModel):
    title = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Article tags'
        verbose_name = 'Article tag'


class ArticleTagItem(DefaultModel):
    tag = models.ForeignKey(ArticleTag, on_delete=models.CASCADE)
    post = models.ForeignKey(Article, on_delete=models.CASCADE)
