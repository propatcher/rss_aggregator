from fastapi import APIRouter

router = APIRouter(
    prefix="/article",
    tags=["Новостные статьи"]
)