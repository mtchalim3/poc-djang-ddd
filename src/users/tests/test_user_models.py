from users.core.models import User


def test_user_model():
    user = User(email="l9v3h@example.com", is_active=True)
    print(user)
    assert user.email == "l9v3h@example.com"
    assert user.is_active
