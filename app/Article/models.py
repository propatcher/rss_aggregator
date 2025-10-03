from app.database import Base
from sqlalchemy import JSON, DateTime, String, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import AnyUrl
from datetime import datetime,timezone

def utc_now():
    return datetime.now(timezone.utc)

class Article(Base):
    __tablename__ = 'articles'
    
    id: Mapped[int] = mapped_column(primary_key=True,index=True)
    feed_id: Mapped[int] = mapped_column(ForeignKey("feeds.id"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(String(2000), nullable=True)
    link: Mapped[str] = mapped_column(String(255), nullable=False,unique=True)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean,default=False)
    tags: Mapped[JSON] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    
    feed: Mapped["Feed"] = relationship("Feed",back_populates='articles')
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.title}')>"
    
    __table_args__ = (
        UniqueConstraint('feed_id', 'link', name='uq_feed_link'),
    )