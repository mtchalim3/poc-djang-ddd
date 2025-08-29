import uuid
from datetime import datetime
import re


class User:
    """
    Modèle métier pur (indépendant de Django).
    Toute la logique de validation et règles métier devrait être ici.
    """

    EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    def __init__(
        self,
        email: str,
        password="Password123@#",
        is_active: bool = True,
        created_at: datetime = None,
    ):
        self.id = str(uuid.uuid4())
        self.password = password
        self.email = self._validate_email(email)
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.seen = set()

    def __repr__(self):
        return f"User(id={self.id}, email={self.email}, is_active={self.is_active}, created_at={self.created_at})"

    def __eq__(self, value):
        if isinstance(value, User):
            return self.id == value.id
        return False

    def __hash__(self):
        return hash(self.id)  # mieux basé sur l'id unique que l'email

    # ---------- Méthodes métier ----------
    def _validate_email(self, email: str) -> str:
        if not re.match(self.EMAIL_REGEX, email):
            raise ValueError("Email invalide")
        return email.lower().strip()

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
