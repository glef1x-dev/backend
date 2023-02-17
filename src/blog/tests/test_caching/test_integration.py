import pytest
from typing import List

from rest_framework.status import HTTP_200_OK

from django.core.cache import cache
from django.urls import reverse

from app.conf.env_reader import env
from app.testing import ApiClient
from blog.models import Article
from blog.tests.factories import ArticleFactory

pytestmark = pytest.mark.django_db


@pytest.fixture()
def articles_batch() -> List[Article]:
    # TODO remove hardcoded batch size
    # basically 2 pages by 8 elements
    articles: List[Article] = ArticleFactory.create_batch(size=16)

    yield articles

    for article in articles:
        article.delete()


@pytest.fixture(autouse=True)
def use_redis_cache_backend(settings):
    settings.CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": env.str("REDIS_URL", "redis://127.0.0.1:6379"),
        }
    }


@pytest.mark.usefixtures("articles_batch")
def test_cache_takes_into_account_pagination_params(as_anon: ApiClient):
    response1 = as_anon.get(
        reverse("v1:blog:article-list"),
        format="json",
        expected_status=HTTP_200_OK,
    )

    assert cache.get("articles") is not None

    next_url = response1.data["next"]
    response2 = as_anon.get(next_url, format="json", expected_status=HTTP_200_OK)

    assert response1.data != response2.data
