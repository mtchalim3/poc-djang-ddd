from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterUserCommand:
    email: str
    password: str
