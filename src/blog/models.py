from django_extensions.db.fields import AutoSlugField
from rest_framework.exceptions import ValidationError

from django.contrib.postgres.indexes import HashIndex
from django.db import models

from app.models import DefaultModel
from app.models import TimestampedModel


class Article(TimestampedModel):
    title = models.CharField(
        max_length=120, verbose_name="Title of the article", db_index=True
    )
    description = models.CharField(
        verbose_name="Description of the article", null=False, max_length=300
    )
    body = models.TextField(default="hello world", verbose_name="Article content")
    image = models.ImageField(verbose_name="image of the post", null=False)
    tags = models.ManyToManyField(
        "ArticleTag", through="ArticleTagItem", related_name="articles"
    )
    slug = AutoSlugField(null=False, blank=False, populate_from="title")
    likes = models.ManyToManyField("ArticleLike", related_name="articles")

    def clean(self) -> None:
        if self.pk is None:
            return

        if self.tags.count() < 1:
            raise ValidationError("There is should be at least one tag specified.")

    class Meta:
        verbose_name_plural = "Articles"
        verbose_name = "Article"
        indexes = [HashIndex(fields=["slug"])]


class ArticleLike(TimestampedModel):
    ip_address = models.GenericIPAddressField(null=True)
    browser_fingerprint = models.TextField()


class ArticleTag(DefaultModel):
    title = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Article tags"
        verbose_name = "Article tag"


class ArticleTagItem(DefaultModel):
    tag = models.ForeignKey(ArticleTag, on_delete=models.CASCADE)
    post = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("tag", "post")
