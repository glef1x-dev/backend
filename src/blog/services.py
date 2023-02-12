from typing import Any

from django.db import transaction

from blog.models import Article
from blog.models import ArticleLike
from blog.models import ArticleTag
from blog.models import ArticleTagItem
from common.orm_utils import create_m2m_related_objects


@transaction.atomic
def create_article(**kwargs: Any) -> Article:
    tags = kwargs.pop("tags")
    likes = kwargs.pop("likes", None)

    article = Article.objects.create(**kwargs)

    create_m2m_related_objects(
        tags,
        first_related_model_instance=article,
        second_related_model_cls=ArticleTag,
        through_model_cls=ArticleTagItem,
    )

    if likes:
        create_m2m_related_objects(
            likes,
            first_related_model_instance=article,
            second_related_model_cls=ArticleLike,
            through_model_cls=article.likes.through,
        )

    article.full_clean()
    return article
