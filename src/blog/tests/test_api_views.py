import pytest

from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.status import HTTP_404_NOT_FOUND

from django.forms.models import model_to_dict
from django.urls import reverse

from app.testing import ApiClient
from blog.models import Article
from blog.tests.utils.files import file_to_base64

pytestmark = pytest.mark.django_db


def test_retrieve_articles(as_anon: ApiClient, article: Article):
    response = as_anon.get(
        reverse("v1:blog:article-list"), format="json", expected_status=HTTP_200_OK
    )
    assert response.data["count"] == 1
    first_blog_post_from_results = response.data["results"][0]
    assert first_blog_post_from_results["slug"] == article.slug
    assert first_blog_post_from_results["title"] == article.title
    assert first_blog_post_from_results[
        "created"
    ] == article.created.isoformat().replace("+00:00", "Z")


def test_create_article(as_user: ApiClient, article: Article):
    # If we won't delete this, the test will fail with "already created"
    # because pytest-factoryboy stores all factory artifacts in database
    article.delete()

    article_dict = model_to_dict(article, exclude=["image"])
    article_dict["image"] = file_to_base64(article.image)

    as_user.post(
        reverse("v1:blog:article-list"),
        article_dict,
        format="json",
        expected_status=HTTP_201_CREATED,
    )

    assert Article.objects.filter(title=article.title).exists()


def test_create_article_that_already_exists(as_user: ApiClient, article: Article):
    article_dict = model_to_dict(article, exclude=["image"])
    article_dict["image"] = file_to_base64(article.image)
    article_dict["tags"] = [model_to_dict(tag) for tag in article_dict["tags"]]

    as_user.post(
        reverse("v1:blog:article-list"),
        article_dict,
        format="json",
        expected_status=HTTP_201_CREATED,
    )


def test_delete_article(as_user: ApiClient, article: Article):
    as_user.delete(
        reverse("v1:blog:article-detail", kwargs={"slug": article.slug}),
        format="json",
        expected_status=HTTP_204_NO_CONTENT,
    )

    assert not Article.objects.filter(slug=article.pk).exists()


def test_delete_article_that_does_not_exists(as_user: ApiClient):
    as_user.delete(
        reverse("v1:blog:article-detail", kwargs={"slug": "sfaz"}),
        format="json",
        expected_status=HTTP_404_NOT_FOUND,
    )


def test_get_single_article(as_anon: ApiClient, article: Article):
    response = as_anon.get(
        reverse("v1:blog:article-detail", kwargs={"slug": article.slug}),
        format="json",
        expected_status=HTTP_200_OK,
    )
    assert response.data["slug"] == article.slug


def test_get_single_article_that_does_not_exist(as_user: ApiClient):
    as_user.get(
        reverse("v1:blog:article-detail", kwargs={"slug": "ababa"}),
        format="json",
        expected_status=HTTP_404_NOT_FOUND,
    )
