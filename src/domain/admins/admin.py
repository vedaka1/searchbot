import uuid
from dataclasses import dataclass


@dataclass
class Admin:
    id: uuid.UUID
    telegram_id: int
    username: str

    @staticmethod
    def create(telegram_id: int, username: str) -> "Admin":
        return Admin(
            id=uuid.uuid4(),
            telegram_id=telegram_id,
            username=username,
        )
