from typing import Optional

from fastapi import APIRouter, Cookie, Depends, Response

from app.exceptions import (
    IncorrectEmailOrPasswordException,
    UserAlreadyExistsException,
    UserAlreadyLogin,
)
from app.User.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from app.User.dao import UserDAO
from app.User.dependencies import get_current_user
from app.User.models import User
from app.User.schemas import SUserLogin, SUserRegistration, SUserResponse

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(user_data: SUserRegistration) -> SUserResponse:
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    user = await UserDAO.add(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
    )
    return SUserResponse(id=user.id, username=user.username, email=user.email)


@router.post("/login")
async def login_user(
    response: Response,
    user_data: SUserLogin,
    rss_access_token: Optional[str] = Cookie(None),
):
    if rss_access_token is not None:
        raise UserAlreadyLogin
    user = await authenticate_user(user_data.identifier, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(
        "rss_access_token",
        access_token,
        httponly=True,
    )

    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("rss_access_token")


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
