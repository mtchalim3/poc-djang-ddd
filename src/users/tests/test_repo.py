import pytest
from users.core.models import User
from users.adapters.repository import InMemoryRepository


@pytest.fixture
def repo():
    return InMemoryRepository()


def test_save_and_get_by_id(repo):
    user = User(email="test@example.com")
    saved_user = repo.save(user)

    assert saved_user.email == "test@example.com"
    assert repo.get_by_id(saved_user.id) == saved_user


def test_exists_and_get_by_email(repo):
    user = User(email="exists@example.com")
    repo.save(user)

    assert repo.exists("exists@example.com") is True
    assert repo.exists("notfound@example.com") is False
    assert repo.get_by_email("exists@example.com") == user


def test_list_users(repo):
    u1 = User(email="a@example.com")
    u2 = User(email="b@example.com")
    repo.save(u1)
    repo.save(u2)

    users = repo.list()
    assert len(users) == 2
    assert u1 in users and u2 in users
