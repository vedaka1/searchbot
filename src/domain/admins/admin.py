import uuid
from dataclasses import dataclass


@dataclass
class Admin:
    telegram_id: int
    username: str
    role: str

    @staticmethod
    def create(telegram_id: int, username: str, role: str = "admin") -> "Admin":
        return Admin(telegram_id=telegram_id, username=username, role=role)
