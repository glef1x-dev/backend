from typing import Dict

import pytest
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.test import APIClient

from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def _enable_django_axes(settings):
    settings.AXES_ENABLED = True


@pytest.fixture
def token_pair(as_anon: APIClient):
    dummy_user = UserFactory.create(password='test')
    return as_anon.post(reverse('v1:a12n:obtain-token'), {
        'username': dummy_user.username,
        'password': 'test',
    }, format='json', expected_status=HTTP_200_OK)


def test_refresh_token(as_anon: APIClient, token_pair: Dict[str, str]):
    response = as_anon.post(reverse('v1:a12n:refresh-token'), {
        'refresh': token_pair['refresh']
    }, format='json', expected_status=HTTP_200_OK)

    assert response['access'] != token_pair['access']


def test_verify_token(as_anon: APIClient, token_pair: Dict[str, str]):
    as_anon.post(reverse('v1:a12n:verify-token'), {
        'token': token_pair['access']
    }, format='json', expected_status=HTTP_200_OK)


@pytest.mark.parametrize('wrong_token', [
    'string',
    'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY1NjA3ODYzLCJpYXQiOjE2NjU2MDc4MDMsImp0aSI6IjZhN2M4OWM5MmNlYjRkZjBhNTdhMTllYzBiMzk3YTQ2IiwidXNlcl9pZCI6Mn0.2goxBUKxQUfLSN3h6AausIsuSWblY2N63H3kmZhvy9naS8htP6NPFpv1ZDWPNo7Ddl8TeMq8JYCkl_Wt4w-zSA '
])
def test_verify_token_failure(as_anon: APIClient, wrong_token: str):
    as_anon.post(reverse('v1:a12n:verify-token'), {
        'token': 'bla-bla-bla'
    }, format='json', expected_status=HTTP_401_UNAUTHORIZED)
