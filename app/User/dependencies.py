from datetime import datetime, timezone

from fastapi import Depends,Request, status
from jose import JWTError, jwt

from app.config import settings
from app.User.dao import UserDAO
from app.User.models import User
from app.exceptions import IncorrectEmailOrPasswordException, IncorrectId, IncorrectIdType, IncorrectRole, TokenAbsentException, TokenJwtException


def get_token(request: Request):
    token = request.cookies.get("rss_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)) -> User:
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        raise TokenJwtException
    
    user_id= payload.get("sub")
    if not user_id:
        raise IncorrectIdType
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise IncorrectId
    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise IncorrectId
    return user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise IncorrectRole
    return current_user
