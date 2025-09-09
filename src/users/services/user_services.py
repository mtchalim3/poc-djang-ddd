import hashlib
from users.core.models import User
from users.core.exceptions import UserAlreadyExists, UserNotFound
from users.core.commands import RegisterUserCommand
from users.adapters.repository import AbstractUserRepository
from users.services.unit_of_work import AbstractUnitOfWork
class UserService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    # ---------- Use Case 1 : Register ----------
    def register(self, cmd: RegisterUserCommand) -> User:
        with self.uow:
            if self.uow.users.exists(cmd.email):
                raise UserAlreadyExists(
                    f"Un utilisateur avec l'email {cmd.email} existe déjà."
                )

            password_hash = self._hash_password(cmd.password)
            user = User(email=cmd.email)
            user.password_hash = password_hash

            saved_user = self.uow.users.save(user)
      
            return saved_user

    # ---------- Use Case 2 : Authenticate ----------
    def authenticate(self, email: str, password: str) -> User:
        with self.uow:
            user = self.uow.users.get_by_email(email)
            if not user:
                raise UserNotFound("Utilisateur introuvable")

            if user.password_hash != self._hash_password(password):
                raise ValueError("Mot de passe incorrect")

            # Pas besoin de commit ici, juste lecture
            return user

    # ---------- Utils ----------
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()