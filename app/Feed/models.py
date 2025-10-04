from typing import List

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Feed(Base):
    __tablename__ = "feeds"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    normalized_url = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    articles: Mapped[List["Article"]] = relationship(
        "Article", back_populates="feed"
    )
    user: Mapped["User"] = relationship("User", back_populates="feeds")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.title}')>"
