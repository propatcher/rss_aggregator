from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError

from app.Article.models import Article
from app.DAO.base_dao import BaseDAO
from app.database import async_session
from app.Feed.models import Feed
from app.logger import logger
from app.User.dependencies import get_current_user
from app.User.models import User


class ArticleDAO(BaseDAO):
    model = Article

    async def get_your_article_by_user(user_id: int):
        try:
            async with async_session() as session:
                query = (
                    select(Article, Article.feed_id)
                    .join(Feed, Feed.id == Article.feed_id)
                    .where(Feed.user_id == user_id)
                )
                result = await session.execute(query)
                if result.scalars().all() == []:
                    return {"У вас нет остлеживаемых rss"}
                return result.scalars().all()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exception"
            msg += ": Cannot get articles"
            extra = {
                "user_id": user_id,
            }
            logger.error(msg, extra=extra)

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
            extra = {
                "article_id": id,
                "user_id": user_id,
            }
            logger.error(msg, extra=extra)
