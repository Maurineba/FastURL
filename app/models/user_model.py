from app.db.base import Base

from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
   __tablename__="users"

   id: Mapped[int] = mapped_column(primary_key=True)
   name: Mapped[str] = mapped_column(String(50))
   email: Mapped[str] = mapped_column(String(50))
   password: Mapped[str] = mapped_column(String(30))

   # urls: Mapped[List["Url"]] = relationship(
   #    back_populates="user"
   # )

   def __repr__(self):
      return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"
