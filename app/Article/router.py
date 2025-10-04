from fastapi import APIRouter, Depends

from app.User.dependencies import get_current_user
from app.User.models import User
from app.Article.dao import ArticleDAO

router = APIRouter(
    prefix="/article",
    tags=["Новостные статьи"]
)

@router.get("")
async def get_your_article(user_data: User = Depends(get_current_user)):
    return await ArticleDAO.get_your_article_by_user(user_data.id)

@router.delete("/delete")
async def delete_your_article(article_id:int,user_data: User = Depends(get_current_user)):
    return await ArticleDAO.delete_your_article_by_id(article_id,user_data.id)