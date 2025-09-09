from django.db import models
import uuid
from users.core.models import User


class UserModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"

    # --- MAPPING ---
    def to_domain(self) -> User:
        user = User(
            email=self.email,
            password=self.password,
            is_active=self.is_active,
            created_at=self.created_at,
        )
        user.id = str(self.id)
        return user

    @classmethod
    def from_domain(cls, user: User) -> "UserModel":
        return cls(
            id=user.id,
            email=user.email,
            password=user.password,
            is_active=user.is_active,
        )
