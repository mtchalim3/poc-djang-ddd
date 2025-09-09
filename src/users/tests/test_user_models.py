from users.core.models import User
from users.core.value_object import Email
from users.core.exceptions import InvalidEmailException

import pytest

def test_user_model():
    user = User(email="l9v3h@example.com", is_active=True)
    print(user)
    assert user.email == "l9v3h@example.com"
    assert user.is_active

