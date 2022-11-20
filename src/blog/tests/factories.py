import pathlib
from typing import List

import factory
import pytest
import pytest_factoryboy
from django.core.files.base import ContentFile, File

from blog.models import ArticleTag, Article

_BASE_DIR = pathlib.Path(__file__).parent.resolve()


@pytest_factoryboy.register(name='article_tag')
class ArticleTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ArticleTag

    title = factory.Sequence(lambda n: 'Tag #%s' % n)


@pytest_factoryboy.register(name='article')
class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    title = 'test'
    description = 'test'
    body = 'test'

    @factory.post_generation
    def tags(self, create: bool, extracted: List[ArticleTag]) -> None:
        if not create:
            return

        if extracted:
            for article_tag in extracted:
                self.tags.add(article_tag)


@pytest.fixture
def article__tags(article_tag: ArticleTag):
    """
    Override article tags because there is no other way
    to inject them to pytest_factoryboy except for creating a fixture
    """
    return [article_tag]


@pytest.fixture
def article__image() -> File:
    image_name = 'blue-square.jpg'
    with open(_BASE_DIR / "media" / image_name, "rb") as file:
        return File(ContentFile(file.read()), image_name)
