import pathlib
import pytest
from typing import List

from _pytest.fixtures import fixture
import factory
import pytest_factoryboy

from django.conf import LazySettings

from blog.models import Article
from blog.models import ArticleLike
from blog.models import ArticleTag

_BASE_TESTS_DIR = pathlib.Path(__file__).parent.resolve()


@pytest.fixture(autouse=True)
def change_media_root_directory(settings: LazySettings):
    settings.MEDIA_ROOT = _BASE_TESTS_DIR / "media"


@pytest_factoryboy.register(name="article_tag")
class ArticleTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ArticleTag

    title = factory.Sequence(lambda n: "Tag #%s" % n)


class ArticleLikeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ArticleLike

    ip_address = factory.Faker('ipv4')
    browser_fingerprint = "fake_fingerprint"


@pytest_factoryboy.register(name="article")
class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article
        exclude = ('images',)

    title = "test"
    description = "test"
    body = "test"
    image = factory.django.ImageField(color='blue')

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


@fixture(autouse=True, scope='session')
def my_fixture():
    yield

    # Garbage collecting all images used in tests
    for file_like in (_BASE_TESTS_DIR / "media").glob("*"):
        if file_like.is_file():
            file_like.unlink()
