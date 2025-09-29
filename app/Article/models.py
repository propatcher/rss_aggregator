from app.database import Base
from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Article(Base):
    __tablename__ = 'articles'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    feed_id: Mapped[int] = mapped_column(ForeignKey("feeds.id"))
    title: Mapped[str] = mapped_column(String(20))
    summary: str (описание, может быть пустым)
    link: str (уникальная ссылка на оригинал)
    published_at: datetime
    is_read: bool = False
    tags: JSON (список строк, например: ["python", "backend"])
    created_at: datetime (когда добавлено в БД)