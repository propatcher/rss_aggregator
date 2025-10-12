from typing import List
from fastapi import APIRouter, Depends, Query

from app.Article.dao import ArticleDAO
from app.Article.schemas import SArticle
from app.User.dependencies import get_current_user
from app.User.models import User
from app.tasks.tasks import sync_all_feeds

router = APIRouter(prefix="/article", tags=["Новостные статьи"])


@router.post("/")
async def get_all_your_article(user_data: User = Depends(get_current_user)):
    return await ArticleDAO.get_your_article_by_user(user_data.id)

@router.post("/by-tag")
async def get_articles_by_tag(
    tag: str = Query(..., min_length=1, description="Тег для фильтрации"),
    user_data: User = Depends(get_current_user)
) -> List[SArticle]:
    return await ArticleDAO.get_articles_by_tag(user_id=user_data.id, tag=tag)

@router.post("/search")
async def search_your_articles(q = Query(None, description="Поиск..."),user_data: User = Depends(get_current_user)):
    return await ArticleDAO.search_find(q,user_data.id)

@router.post("/refresh")
async def refresh_your_articles(user_data: User = Depends(get_current_user)):
    sync_all_feeds()
    return await ArticleDAO.get_your_article_by_user(user_data.id)


@router.delete("/delete")
async def delete_your_article(
    article_id: int, user_data: User = Depends(get_current_user)
):
    return await ArticleDAO.delete_your_article_by_id(article_id, user_data.id)
