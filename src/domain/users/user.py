from dataclasses import dataclass


@dataclass
class User:
    telegram_id: int
    username: str
    role: str

    @staticmethod
    def create(telegram_id: int, username: str = "", role: str = "user") -> "User":
        return User(telegram_id=telegram_id, username=username, role=role)
