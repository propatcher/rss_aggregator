from typing import List
from app.database import Base
from sqlalchemy import DateTime, ForeignKey,String
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String(20),unique=True, nullable=False,index=True)
    email: Mapped[str] = mapped_column(String(100),unique=True,nullable=False,index=True)
    hashed_password: Mapped[str] = mapped_column(String(255),nullable=False)
    
    feeds: Mapped[List["Feed"]] = relationship("Feed",back_populates='user')
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"