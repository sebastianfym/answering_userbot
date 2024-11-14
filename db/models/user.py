import datetime
from sqlalchemy import Enum, DateTime, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from db.models.status import Status


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(Enum(Status), default=None)
    status_updated_at: Mapped[datetime.datetime] = mapped_column(DateTime)

    def __repr__(self):
        return f"User(id={self.id}, chat_id={self.chat_id}, " \
               f"created_at={self.created_at}, status={self.status}, " \
               f"status_updated_at={self.status_updated_at})"

