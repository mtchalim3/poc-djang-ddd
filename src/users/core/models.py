import uuid
from datetime import datetime
from users.core.value_object import Email


class User:
    """
    Modèle métier pur (indépendant de Django).
    Toute la logique de validation et règles métier devrait être ici.
    """


    def __init__(
        self,
        email: Email,
        password="Password123@#",
        is_active: bool = True,
        created_at: datetime = None,
    ):
        self.id = str(uuid.uuid4())
        self.password = password
        self._email = email
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
    @property
    def email(self) -> str:
        return str(self._email)

    @email.setter
    def email(self, value: str | Email) -> None:
        if isinstance(value, Email):
            self._email = value
        else:
            self._email = Email(value)




    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
