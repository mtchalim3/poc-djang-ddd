from users.core.models import User
from account.models import UserModel
from users.adapters.repository import AbstractUserRepository
from typing import Optional, List


class DjangoUserRepository(AbstractUserRepository):
    def exists(self, email: str) -> bool:
        return UserModel.objects.filter(email=email).exists()

    def _get_by_email(self, email: str) -> Optional[User]:
        obj = UserModel.objects.filter(email=email).first()
        return obj.to_domain() if obj else None

    def _get_by_id(self, user_id: str) -> Optional[User]:
        obj = UserModel.objects.filter(id=user_id).first()
        return obj.to_domain() if obj else None

    def _list(self) -> List[User]:
        return [u.to_domain() for u in UserModel.objects.all()]

    def _save(self, user: User) -> User:
        obj = UserModel.from_domain(user)
        obj.save()
        return obj.to_domain()

    def _exists(self, email: str) -> bool:
        return self.exists(email)
