import asyncio
from httpx import AsyncClient, RequestError, TimeoutException
from pydantic import HttpUrl
from sqlalchemy import delete, select, update
from app.DAO.base_dao import BaseDAO
from app.Feed.models import Feed
from app.database import async_session
from sqlalchemy.exc import SQLAlchemyError
from app.logger import logger

import feedparser

from app.exceptions import FeedNotFound, InvalidRssLink, RssLinkAlreadyExist, RssLinkAlreadyFollow

def _is_valid_rss_content(content: bytes) -> bool:
    try:
        feed = feedparser.parse(content)
        has_entries = len(feed.entries) > 0
        has_title = bool(feed.feed.get('title'))
        is_rss_or_atom = (
            feed.version.startswith('rss') or
            feed.version.startswith('atom')
        ) if feed.version else False
        return has_entries and (has_title or is_rss_or_atom)
    except Exception:
        return False


async def is_valid_rss(url: str) -> bool:
    try:
        async with AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers={"User-Agent": "RSS Aggregator"})
            response.raise_for_status()
            
            content_type = response.headers.get('content-type', '').lower()
            if 'html' in content_type and 'xml' not in content_type:
                return False

            loop = asyncio.get_event_loop()
            is_valid = await loop.run_in_executor(
                None, _is_valid_rss_content, response.content
            )
            return is_valid

    except (TimeoutException, RequestError, Exception):
        return False


def normalize_url(url: HttpUrl) -> str:
    host = str(url.host).lower() if url.host else ""
    path = url.path or "/"
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    return f"{host}{path}"


class FeedDAO(BaseDAO):
    model = Feed
    
    async def add_feed(user_id: int, url: HttpUrl, title: str):
        try:
            normalized = normalize_url(url)
            
            if not await is_valid_rss(str(url)):
                raise InvalidRssLink

            async with async_session() as session:
                find_query = select(Feed).where(
                    Feed.normalized_url == normalized,
                    Feed.user_id == user_id,
                )
                result = await session.execute(find_query)
                if result.scalar_one_or_none():
                    raise RssLinkAlreadyExist

                new_feed = Feed(
                    user_id=user_id,
                    url=str(url),
                    normalized_url=normalized,
                    title=title,
                    is_active=True
                )
                session.add(new_feed)
                await session.flush()
                await session.commit()
                return new_feed
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exception"
            msg += ": Cannot add feed"
            extra = {
                "user_id": user_id,
                "url": url,
                "title": title
            }
            logger.error(
                msg, extra=extra
            )
    async def delete_feed(feed_id:int,user_id:int):
        try:
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
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exception"
            msg += ": Cannot add feed"
            extra = {
                "feed_id": feed_id,
                "user_id": user_id,
            }
            logger.error(
                msg, extra=extra
            )
        
    async def update_feed(user_id: int, old_url: HttpUrl, new_title: str, new_url: HttpUrl):
        try:
            new_normalized = normalize_url(new_url)

            if not await is_valid_rss(str(new_url)):
                raise InvalidRssLink

            async with async_session() as session:
                old_normalized = normalize_url(old_url)
                result = await session.execute(
                    select(Feed).where(
                        Feed.normalized_url == old_normalized,
                        Feed.user_id == user_id,
                    )
                )
                feed = result.scalar_one_or_none()
                if not feed:
                    raise FeedNotFound

                existing_feed = await session.execute(
                    select(Feed).where(
                        Feed.normalized_url == new_normalized,
                        Feed.user_id == user_id,
                    )
                )
                if existing_feed.scalar_one_or_none() and str(new_url) != feed.url:
                    raise RssLinkAlreadyFollow

                feed.url = str(new_url)
                feed.normalized_url = new_normalized
                feed.title = new_title

                await session.commit()
                await session.refresh(feed)
                return feed
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exception"
            msg += ": Cannot add feed"
            extra = {
                "user_id": user_id,
                "old_url": old_url,
                "new_title":new_title,
                "new_url":new_url
            }
            logger.error(
                msg, extra=extra
            )