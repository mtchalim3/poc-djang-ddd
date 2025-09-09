from abc import ABC, abstractmethod
from users.adapters.repository import AbstractUserRepository, InMemoryRepository
from users.adapters.django_repository import DjangoUserRepository


class AbstractUnitOfWork(ABC):
    users: AbstractUserRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class DjangoUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.users = DjangoUserRepository()

    def __enter__(self):
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)

    def commit(self):

        pass

    def rollback(self):

        pass


class InMemoryUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.users = InMemoryRepository()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass  # rien à rollback

    def commit(self):
        pass  # pas de DB réelle

    def rollback(self):
        pass
