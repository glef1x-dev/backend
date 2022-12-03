from typing import Any, Iterable, Iterator, TypeVar

from django.db import transaction

from blog.models import Article
from blog.models import ArticleTag
from blog.models import ArticleTagItem

_T = TypeVar("_T")


@transaction.atomic
def create_article(**kwargs: Any) -> Article:
    tags = kwargs.pop("tags")
    article = Article.objects.create(**kwargs)
    article_tags = tuple(
        _only_first_element_from_tuples(
            ArticleTag.objects.get_or_create(**tag) for tag in tags
        )
    )

    article_tag_to_tag_associations = [
        ArticleTagItem(tag=tag, post=article) for tag in article_tags
    ]
    Article.tags.through.objects.bulk_create(article_tag_to_tag_associations)
    return article


def _only_first_element_from_tuples(collection: Iterable[_T]) -> Iterator[_T]:
    return map(lambda o: o[0], collection)
