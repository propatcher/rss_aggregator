from typing import Optional
from sqlalchemy import delete, func, select, text
from sqlalchemy.exc import SQLAlchemyError

from app.Article.models import Article
from app.DAO.base_dao import BaseDAO
from app.database import async_session
from app.Feed.models import Feed
from app.exceptions import NoArticle
from app.logger import logger
from app.User.dependencies import get_current_user
from app.User.models import User
from sqlalchemy.orm import joinedload

class ArticleDAO(BaseDAO):  #TODO Больше обработок exception
    model = Article

    async def get_your_article_by_user(user_id: int):
        try:
            async with async_session() as session:
                query = (
                select(Article)
                    .options(joinedload(Article.feed))
                    .join(Feed, Feed.id == Article.feed_id)
                    .where(Feed.user_id == user_id)
                )
                result = await session.execute(query)
                articles = result.scalars().all()
                if not articles:
                    raise NoArticle
                return articles
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exception"
                msg += ": Cannot get articles"
            else:
                msg = f"Unexpected Exception ({type(e).__name__})"                
            extra = {
                "user_id": user_id,
            }
            logger.error(msg, extra=extra)
            raise

    async def delete_your_article_by_id(id: int, user_id: int):
        try:
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
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exception"
                msg += ": Cannot delete articles"
            else:
                msg = f"Unexpected Exception ({type(e).__name__})"                
            extra = {
                "article_id": id,
                "user_id": user_id,
            }
            logger.error(msg, extra=extra)
            raise
    
    async def get_articles_by_tag(user_id, tag):    #TODO Я ЧЕСТНО НЕ ЗНАЮ ПОЧЕМУ ОН БЕРЕТ ТОЛЬКО ОДНУ СТАТЬЮ И ТУ ВЫБИРАЕТ СЛУЧАЙНО(ТЕСТЫ)
        try:
            async with async_session() as session:
                query = (
                select(Article)
                    .options(joinedload(Article.feed))
                    .join(Feed, Feed.id == Article.feed_id)
                    .where(Feed.user_id == user_id)
                    .where(Article.tags.contains([tag]))
                )
                result = await session.execute(query)
                articles = result.scalars().all()
                if not articles:
                    raise NoArticle
                return articles
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exception"
                msg += ": Cannot get articles"
            else:
                msg = f"Unexpected Exception ({type(e).__name__})"                
            extra = {
                "user_id": user_id,
                "tag": tag
            }
            logger.error(msg, extra=extra)
            raise
    async def search_find(search_params: Optional[str], user_id: int):
        try:
            async with async_session() as session:
                query = (
                    select(Article)
                    .options(joinedload(Article.feed))
                    .join(Feed, Feed.id == Article.feed_id)
                    .where(Feed.user_id == user_id)
                )
                if search_params:
                    search_pattern = f"%{search_params}%"
                    query = query.where(Article.title.ilike(search_pattern))
                
                result = await session.execute(query)
                articles = result.unique().scalars().all()
                
                if not articles:
                    raise NoArticle
                    
                return articles
                
        except NoArticle:
            raise
        
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exception"
                msg += ": Cannot get articles"
            else:
                msg = f"Unexpected Exception ({type(e).__name__})"                
            extra = {
                "user_id": user_id,
                "search_params": search_params
            }
            logger.error(msg, extra=extra)
            raise