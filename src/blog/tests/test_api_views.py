import pytest
from django.forms.models import model_to_dict
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from app.testing import ApiClient
from blog.models import Article

pytestmark = pytest.mark.django_db


def test_retrieve_articles(as_anon: ApiClient, article: Article):
    response = as_anon.get(reverse('v1:blog:retrieve-or-create-articles'),
                           format='json', expected_status=HTTP_200_OK)
    assert response['count'] == 1
    first_blog_post_from_results = response['results'][0]
    assert first_blog_post_from_results['id'] == article.pk
    assert first_blog_post_from_results['title'] == article.title
    assert first_blog_post_from_results['created'] == article.created.isoformat().replace(
        '+00:00', 'Z'
    )


def test_create_article(as_user: ApiClient, article: Article):
    # If we won't delete this, the test will fail with "already created"
    # because pytest-factoryboy stores all factory artifacts in database
    article.delete()

    as_user.post(reverse('v1:blog:retrieve-or-create-articles'), model_to_dict(
        article,
        exclude=['image']
    ), format='json', expected_status=HTTP_201_CREATED)

    assert Article.objects.filter(title=article.title).exists()


def test_create_article_that_already_exists(as_user: ApiClient, article: Article):
    as_user.post(reverse('v1:blog:retrieve-or-create-articles'), model_to_dict(
        article,
        exclude=['image']
    ), format='json', expected_status=HTTP_201_CREATED)


def test_delete_article(as_user: ApiClient, article: Article):
    as_user.delete(reverse('v1:blog:delete-article', kwargs={'pk': article.pk}),
                   format='json', expected_status=HTTP_204_NO_CONTENT)

    assert not Article.objects.filter(pk=article.pk).exists()


def test_delete_article_that_does_not_exists(as_user: ApiClient):
    as_user.delete(reverse('v1:blog:delete-article', kwargs={'pk': 2343242}),
                   format='json', expected_status=HTTP_404_NOT_FOUND)


def test_get_single_article(as_anon: ApiClient, article: Article):
    blog_post_json = as_anon.get(
        reverse('v1:blog:retrieve-article',
                kwargs={
                    'pk': article.pk
                }),
        format='json',
        expected_status=HTTP_200_OK
    )
    assert blog_post_json['id'] == article.pk


def test_get_single_article_that_does_not_exist(as_user: ApiClient):
    as_user.get(
        reverse('v1:blog:retrieve-article',
                kwargs={
                    'pk': 24324
                }),
        format='json',
        expected_status=HTTP_404_NOT_FOUND
    )
