from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.models.base import Base


class UserModel(Base):
    __tablename__ = "users"
    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(nullable=True)
    role: Mapped[str]
