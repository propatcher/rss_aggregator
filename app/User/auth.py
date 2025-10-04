from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Cookie, Depends
from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.User.dao import UserDAO
from app.User.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(identifier: str, password: str) -> Optional[User]:
    user = await UserDAO.find_by_email_or_username(identifier)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
