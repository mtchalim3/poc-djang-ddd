import pytest
from users.services.user_services import UserService
from users.adapters.django_repository import DjangoUserRepository
from users.services.unit_of_work import DjangoUnitOfWork
from users.core.commands import RegisterUserCommand
from users.core.exceptions import UserAlreadyExists, UserNotFound

pytestmark = pytest.mark.django_db


@pytest.fixture
def service():
    return UserService(DjangoUnitOfWork())


def test_register_user(service):
    cmd = RegisterUserCommand(email="new@example.com", password="mypassword")
    user = service.register(cmd)
    assert user.email == "new@example.com"


def test_register_duplicate_user(service):
    cmd = RegisterUserCommand(email="dup@example.com", password="secret")
    service.register(cmd)
    with pytest.raises(UserAlreadyExists):
        service.register(cmd)
