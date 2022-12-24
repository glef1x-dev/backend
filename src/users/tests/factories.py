import factory
import pytest_factoryboy

from users.models import User


@pytest_factoryboy.register(scope="module")
class UserFactory(factory.django.DjangoModelFactory):
    """
    Pytest integrated user factory using pytest-factoryboy
    """

    class Meta:
        model = User

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.PostGenerationMethodCall("set_password", "dumb")
