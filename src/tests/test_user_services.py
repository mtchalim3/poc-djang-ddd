import pytest
from users.core.commands import RegisterUserCommand
from users.services.user_services import UserService
from users.core.exceptions import UserAlreadyExists, UserNotFound
from users.adapters.repository import InMemoryRepository
from users.services.unit_of_work import InMemoryUnitOfWork


@pytest.fixture
def service():
    return UserService(InMemoryUnitOfWork())


def test_register_user(service):
    cmd = RegisterUserCommand(email="test@example.com", password="secret")
    user = service.register(cmd)

    assert user.email == "test@example.com"
    assert hasattr(user, "password_hash")


def test_register_duplicate_user(service):
    cmd = RegisterUserCommand(email="dup@example.com", password="secret")
    service.register(cmd)
    with pytest.raises(UserAlreadyExists):
        service.register(cmd)


def test_authenticate_success(service):
    cmd = RegisterUserCommand(email="login@example.com", password="mypassword")
    user = service.register(cmd)

    authenticated = service.authenticate("login@example.com", "mypassword")
    assert authenticated == user


def test_authenticate_fail(service):
    cmd = RegisterUserCommand(email="fail@example.com", password="rightpass")
    service.register(cmd)

    with pytest.raises(ValueError):  # mauvais password
        service.authenticate("fail@example.com", "wrongpass")

    with pytest.raises(UserNotFound):  # mauvais email
        service.authenticate("notfound@example.com", "whatever")
