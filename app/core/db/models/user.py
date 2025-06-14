from app.core.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Integer, String
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
