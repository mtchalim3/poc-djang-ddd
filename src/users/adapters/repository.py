from abc import ABC, abstractmethod
from typing import Optional, List
from users.core.models import User
from typing import Optional, List


class AbstractUserRepository(ABC):
    """Interface du UserRepository dans le domaine"""

    def exists(self, email: str) -> bool:
        return self._exists(email)

    def get_by_email(self, email: str) -> Optional[User]:
        return self._get_by_email(email)

    def update(self, user: User) -> User:
        return self._save(user)

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self._get_by_id(user_id)

    def list(self) -> List[User]:
        return self._list()

    def save(self, user: User) -> User:
        return self._save(user)

    @abstractmethod
    def _get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def _get_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    def _list(self) -> List[User]:
        pass

    @abstractmethod
    def _save(self, user: User) -> User:
        pass

    @abstractmethod
    def _exists(self, email: str) -> bool:
        pass


class InMemoryRepository(AbstractUserRepository):
    def __init__(self):
        self._users = []

    def _exists(self, email: str) -> bool:
        return any(user.email == email for user in self._users)

    def _get_by_email(self, email: str) -> Optional[User]:
        return next((user for user in self._users if user.email == email), None)

    def _get_by_id(self, user_id: str) -> Optional[User]:
        return next((user for user in self._users if user.id == user_id), None)

    def _list(self) -> List[User]:
        return self._users

    def _save(self, user: User) -> User:
        self._users.append(user)
        return user
