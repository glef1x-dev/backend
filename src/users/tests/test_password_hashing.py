import uuid

import pytest

from users.models import User

pytestmark = [pytest.mark.django_db]


def test():
    user = User.objects.create(username=str(uuid.uuid4()))
    user.set_password('l0ve')

    user.save()

    assert user.password.startswith('argon2')
