from app.database import Base
from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Feed(Base):
    __tablename__ = 'feeds'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    user: Mapped["User"] = relationship("User", back_populates="feeds")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"