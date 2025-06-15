from app.core.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.types import Integer, String

class Sheets(Base):
    __tablename__ = "sheets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    sheets_id: Mapped[str] = mapped_column(String, index=True, unique=True)
    telegram_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.telegram_id"), index=True)