from fastapi import HTTPException
from pydantic import HttpUrl
from sqlalchemy import delete, select, update
from app.DAO.base_dao import BaseDAO
from app.Feed.models import Feed
from app.database import async_session


def normalize_url(url: HttpUrl) -> str:
    host = str(url.host).lower() if url.host else ""
    path = url.path or "/"
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    return f"{host}{path}"

class FeedDAO(BaseDAO):
    model = Feed
    
    async def add_feed(user_id: int, url: HttpUrl, title: str):
        normalized = normalize_url(url)
        async with async_session() as session:
            find_query = select(Feed).where(
                Feed.normalized_url == normalized,
                Feed.user_id == user_id,
            )
            result = await session.execute(find_query)
            if result.scalar_one_or_none():
                raise HTTPException(status_code=409, detail="Вы уже отслеживаете эту ссылку")

            new_feed = Feed(
                user_id=user_id,
                url=str(url),
                normalized_url=normalized,
                title=title
            )
            session.add(new_feed)
            await session.flush()
            await session.commit()
            return new_feed
    async def delete_feed(feed_id:int,user_id:int):
        async with async_session() as session:
            find_query = select(Feed).where(
                Feed.id == feed_id,
                Feed.user_id == user_id
            )
            result = await session.execute(find_query)
            feed = result.scalar_one_or_none()
            if not feed:
                return False
            delete_stmt = delete(Feed).where(
                Feed.id == feed_id,
                Feed.user_id == user_id
            )
            await session.execute(delete_stmt)
            await session.commit()
            return True
    async def update_feed(user_id: int, url: HttpUrl, new_title: str, new_url):
        normalized = normalize_url(url)
        async with async_session() as session:
            result = await session.execute(
                select(Feed).where(
                    Feed.normalized_url == normalized,
                    Feed.user_id == user_id,
                )
            )
            feed = result.scalar_one_or_none()
            if not feed:
                return False
            feed.url = str(new_url)
            feed.title = new_title
            await session.commit()
            return feed