import pytest

from rest_framework.status import HTTP_200_OK

from django.core.cache import cache
from django.core.cache import caches
from django.urls import reverse

from app.testing import ApiClient
from blog.models import Article
from blog.models import ArticleTag

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def clear_cache():
    caches["default"].clear()


def test_list_articles_add_articles_to_cache(as_anon: ApiClient):
    as_anon.get(
        reverse("v1:blog:article-list"), format="json", expected_status=HTTP_200_OK
    )

    assert cache.get("articles") is not None


def test_retrieve_article_add_article_to_cache(as_anon: ApiClient, article: Article):
    as_anon.get(
        reverse("v1:blog:article-detail", kwargs={"slug": article.slug}),
        format="json",
        expected_status=HTTP_200_OK,
    )

    assert cache.get(f"article:{article.slug}") is not None


def test_cache_invalidation_after_delete_single_article(
    as_user: ApiClient, article: Article
):
    as_user.delete(
        reverse("v1:blog:article-detail", kwargs={"slug": article.slug}), format="json"
    )

    assert cache.get("articles") is None
    assert cache.get(f"article:{article.slug}") is None
    assert all(cache.get(f"articles:{tag.title}") is None for tag in article.tags.all())


def test_cache_invalidation_after_creating_an_article(
    as_user: ApiClient, article: Article
):
    as_user.get(
        reverse("v1:blog:article-list"), format="json", expected_status=HTTP_200_OK
    )
    as_user.delete(
        reverse("v1:blog:article-detail", kwargs={"slug": article.slug}), format="json"
    )

    assert cache.get("articles") is None
    assert cache.get(f"article:{article.slug}") is None
    assert all(cache.get(f"articles:{tag.title}") is None for tag in article.tags.all())


def test_list_articles_add_articles_to_cache_filtered_by_tag(
    as_anon: ApiClient, article_tag: ArticleTag
):
    as_anon.get(
        reverse("v1:blog:article-list"),
        {"tags__title": article_tag.title},
        format="json",
        expected_status=HTTP_200_OK,
    )

    assert cache.get(f"articles:{article_tag.title}") is not None
