from fastapi import APIRouter

router = APIRouter(
    prefix="/feed",
    tags=["Лента новостей"]
)