from datetime import datetime

from app.db.base import Base

from sqlalchemy import String, Integer, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Url(Base):
   __tablename__ = "urls"

   id: Mapped[int] = mapped_column(primary_key=True)
   url: Mapped[str] = mapped_column(String(2048), nullable=False)
   code: Mapped[str] = mapped_column(String(8), nullable=False, unique=True, index=True)
   clicks: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
   shorted_url: Mapped[str] = mapped_column(
      String(80),
      nullable=False,
      unique=True,
      index=True
   )
   created_at: Mapped[datetime] = mapped_column(
      DateTime(timezone=True),
      server_default=func.now()
   )
   expired: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

   def __repr__(self):
      return f"Url(id={self.id!r}, url={self.url!r}, shorted_url={self.shorted_url!r})"
