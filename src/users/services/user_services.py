import hashlib
from users.core.models import User
from users.core.exceptions import UserAlreadyExists, UserNotFound
from users.core.commands import RegisterUserCommand
from users.adapters.repository import AbstractUserRepository


class UserService:
    def __init__(self, repo: AbstractUserRepository):
        self.repo = repo

    def register(self, cmd: RegisterUserCommand) -> User:
        """Créer un nouvel utilisateur"""
        if self.repo.exists(cmd.email):
            raise UserAlreadyExists(
                f"Un utilisateur avec l'email {cmd.email} existe déjà."
            )

        # Hash simple du mot de passe ( pour POC uniquement, pas en prod !)
        password_hash = self._hash_password(cmd.password)

        user = User(email=cmd.email)
        user.password_hash = password_hash  # on enrichit l'entity avec le hash
        return self.repo.save(user)

    def authenticate(self, email: str, password: str) -> User:
        """Vérifier login/password"""
        user = self.repo.get_by_email(email)
        if not user:
            raise UserNotFound("Utilisateur introuvable")

        if user.password_hash != self._hash_password(password):
            raise ValueError("Mot de passe incorrect")

        return user

    # ---------- Utils ----------
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
