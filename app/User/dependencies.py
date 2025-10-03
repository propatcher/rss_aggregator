from datetime import datetime, timezone

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt

from app.config import settings
from app.User.dao import UserDAO
from app.User.models import User


def get_token(request: Request):
    token = request.cookies.get("rss_access_token")
    if not token:
        raise HTTPException(status_code=401)
    return token


async def get_current_user(token: str = Depends(get_token)) -> User:
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        raise HTTPException(status_code=402)
    
    user_id= payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=403,detail="Айди не может загружен")
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Айди не найден")
    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=404,detail="Пользователь не найден")
    return user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return current_user
