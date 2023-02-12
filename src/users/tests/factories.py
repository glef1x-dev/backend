import pytest

import factory

from users.models import User

pytestmark = pytest.mark.django_db


class UserFactory(factory.django.DjangoModelFactory):
    """Pytest integrated user factory using pytest-factoryboy."""

    class Meta:
        model = User

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.PostGenerationMethodCall("set_password", "dumb")


# Here we don't use pytest-factoryboy since it doesn't allow to change the fixture scope
# For more details see https://github.com/pytest-dev/pytest-factoryboy/issues/31
@pytest.fixture(scope="session", name="user")
def create_test_user(django_db_setup, django_db_blocker):
    # It's impossible to use django db in session scoped fixtures without
    # requesting django_db_setup and django_db_blocker fixtures
    # https://stackoverflow.com/questions/62722599/how-can-i-use-pytest-django-to-create-a-user-object-only-once-per-session
    with django_db_blocker.unblock():
        return UserFactory.create(password="test")
