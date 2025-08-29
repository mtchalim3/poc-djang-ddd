import pytest
from users.adapters.django_repository import DjangoUserRepository
from users.core.models import User
from interface_django.account.models import UserModel

pytestmark = pytest.mark.django_db  # important pour utiliser la DB Django


def test_save_and_get_user():
    repo = DjangoUserRepository()
    user = User(email="django@example.com", password="123456")

    saved_user = repo.save(user)

    assert saved_user.email == "django@example.com"
    assert repo.exists("django@example.com")


def test_get_by_email_returns_user():
    repo = DjangoUserRepository()
    user = User(email="test2@example.com", password="pwd")
    repo.save(user)

    fetched = repo.get_by_email("test2@example.com")

    assert fetched is not None
    assert fetched.email == "test2@example.com"


def test_list_users():
    repo = DjangoUserRepository()
    repo.save(User(email="u1@example.com", password="p1"))
    repo.save(User(email="u2@example.com", password="p2"))

    users = repo.list()
    assert len(users) == 2
