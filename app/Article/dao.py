
from fastapi import Depends
from sqlalchemy import delete, select
from app.Article.models import Article
from app.DAO.base_dao import BaseDAO
from app.Feed.models import Feed
from app.User.dependencies import get_current_user
from app.User.models import User
from app.database import async_session

class ArticleDAO(BaseDAO):
    model = Article
    
    async def get_your_article_by_user(user_id : int):
        async with async_session() as session:
            query = (
                select(Article, Article.feed_id)
                .join(Feed, Feed.id == Article.feed_id)
                .where(Feed.user_id == user_id)
            )
            result = await session.execute(query)
            return result.scalars().all()
    async def delete_your_article_by_id(id:int,user_id:int):
        async with async_session() as session:
            query = (
                delete(Article)
                .where(Article.id == id)
                .where(Article.feed_id == Feed.id)
                .where(Feed.user_id == user_id)
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount
                