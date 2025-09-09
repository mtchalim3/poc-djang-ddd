import re
from dataclasses import dataclass
import uuid

from users.core.exceptions import InvalidPasswordException, InvalidOperation, InvalidEmailException


@dataclass(frozen=True)
class Email:
    value: str

    
    def __post_init__(self):
        if not isinstance(self.value, str):
            raise TypeError("Email must be a string")
        if not self._is_valid_email(self.value):
            print(self._is_valid_email(self.value))
            raise InvalidEmailException(f"Invalid email format: {self.value}")

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        # Regex RFC 5322 simplifiée
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return re.match(pattern, email) is not None

    def masked(self) -> str:
        """Masque partiellement l'email pour affichage sécurisé."""
        user, domain = self.value.split("@")
        return f"{user[0]}***@{domain}"

    def __str__(self) -> str:
        return self.value





@dataclass(frozen=True)
class UserID:
    """Value Object représentant l'identifiant unique d'un User."""

    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise TypeError("UserID must be a string")
        try:
            uuid.UUID(self.value)
        except ValueError:
            raise ValueError(f"Invalid UserID: {self.value}")

    @classmethod
    def new(cls) -> "UserID":
        """Générer un nouvel ID unique."""
        return cls(str(uuid.uuid4()))

    def __str__(self):
        return self.value


@dataclass(frozen=True)
class Password:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise TypeError("Password must be a string")
        if not self._is_valid(self.value):
            raise InvalidPasswordException(
                "Password does not meet security requirements"
            )

    @staticmethod
    def _is_valid(pwd: str) -> bool:
        return (
            len(pwd) >= 8
            and re.search(r"[A-Z]", pwd)
            and re.search(r"[a-z]", pwd)
            and re.search(r"\d", pwd)
            and re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd)
        )

    def __str__(self):
        return self.value


class FirstName(str):
    def __new__(cls, value: str):
        if not isinstance(value, str):
            raise InvalidOperation("First name must be a string")
        if not value.strip():
            raise InvalidOperation("First name cannot be empty")
        return str.__new__(cls, value.strip())


class LastName(str):
    def __new__(cls, value: str):
        if not isinstance(value, str):
            raise InvalidOperation("Last name must be a string")
        if not value.strip():
            raise InvalidOperation("Last name cannot be empty")
        return str.__new__(cls, value.strip())
