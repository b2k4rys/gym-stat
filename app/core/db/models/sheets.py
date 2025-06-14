from app.core.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.types import Integer, String

class Sheets(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    sheets_id: Mapped[int] = mapped_column(Integer, index=True, unique=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("usesr.id"), index=True)