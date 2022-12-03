import factory
import pytest_factoryboy

from users.models import User


@pytest_factoryboy.register
class UserFactory(factory.django.DjangoModelFactory):
    """
    Pytest integrated user factory using pytest-factoryboy
    """

    class Meta:
        model = User

    username = "dumb"
    first_name = "John"
    last_name = "dumb"
    password = factory.PostGenerationMethodCall("set_password", "dumb")
