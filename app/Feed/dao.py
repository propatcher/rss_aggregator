import asyncio

import feedparser
from httpx import AsyncClient, RequestError, TimeoutException
from pydantic import HttpUrl
from pydantic import HttpUrl, ValidationError
from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError

from app.Article.models import Article
from app.DAO.base_dao import BaseDAO
from app.database import async_session
from app.exceptions import (
    FeedNotFound,
    InvalidRssLink,
    RssLinkAlreadyExist,
    RssLinkAlreadyFollow,
)
from app.Feed.models import Feed
from app.logger import logger


def _is_valid_rss_content(content: bytes) -> bool:
    try:
        feed = feedparser.parse(content)
        has_entries = len(feed.entries) > 0
        has_title = bool(feed.feed.get("title"))
        is_rss_or_atom = (
            (feed.version.startswith("rss") or feed.version.startswith("atom"))
            if feed.version
            else False
        )
        return has_entries and (has_title or is_rss_or_atom)
    except Exception:
        return False


async def is_valid_rss(url: str) -> bool:
    try:
        async with AsyncClient(timeout=10.0) as client:
            response = await client.get(
                url, headers={"User-Agent": "RSS Aggregator"}
            )
            response.raise_for_status()

            content_type = response.headers.get("content-type", "").lower()
            if "html" in content_type and "xml" not in content_type:
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

    async def add_feed(user_id: int, url: str, title: str):
        try:
            clean_url = url.strip()
            if not clean_url:
                raise InvalidRssLink
            try:
                validated_url = HttpUrl(clean_url)
            except ValidationError:
                raise InvalidRssLink
            normalized = normalize_url(validated_url)

            if not await is_valid_rss(str(validated_url)):
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
                    is_active=True,
                )
                session.add(new_feed)
                await session.flush()
                await session.commit()
                return new_feed
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exception"
                msg += ": Cannot add feed"
            else:
                msg = f"Unexpected Exception ({type(e).__name__})"
            extra = {"user_id": user_id, "url": url, "title": title}
            logger.error(msg, extra=extra, exc_info=True)

            raise
        
    async def delete_feed(feed_id: int, user_id: int):
        try:
            async with async_session() as session:
                find_query = select(Feed).where(
                    Feed.id == feed_id, Feed.user_id == user_id
                )
                result = await session.execute(find_query)
                feed = result.scalar_one_or_none()
                if not feed:
                    return False
                delete_stmt = delete(Feed).where(
                    Feed.id == feed_id, Feed.user_id == user_id
                )
                feed_delete_stmt = delete(Article).where(
                    Article.feed_id == feed_id
                )
                await session.execute(feed_delete_stmt)
                await session.execute(delete_stmt)
                await session.commit()
                return True
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exception"
                msg += ": Cannot del feed"
            else:
                msg = f"Unexpected Exception ({type(e).__name__})"
            extra = {
                "feed_id": feed_id,
                "user_id": user_id,
            }
            logger.error(msg, extra=extra)
            raise

    async def update_feed(user_id: int, old_url: str, new_title: str, new_url: str):
        try:
            clean_old_url = old_url.strip()
            clean_new_url = new_url.strip()

            if not clean_old_url or not clean_new_url:
                raise InvalidRssLink

            try:
                validated_old_url = HttpUrl(clean_old_url)
                validated_new_url = HttpUrl(clean_new_url)
            except ValidationError:
                raise InvalidRssLink

            normalized_old = normalize_url(validated_old_url)
            print(normalized_old)
            normalized_new = normalize_url(validated_new_url)

            if not await is_valid_rss(str(validated_new_url)):
                raise InvalidRssLink

            async with async_session() as session:
                result = await session.execute(
                    select(Feed).where(
                        Feed.normalized_url == normalized_old,
                        Feed.user_id == user_id,
                    )
                )
                feed = result.scalar_one_or_none()
                if not feed:
                    raise FeedNotFound

                existing_result = await session.execute(
                    select(Feed).where(
                        Feed.normalized_url == normalized_new,
                        Feed.user_id == user_id,
                    )
                )
                existing = existing_result.scalar_one_or_none()
                if existing and existing.id != feed.id:
                    raise RssLinkAlreadyFollow

                feed.url = str(validated_new_url)
                feed.normalized_url = normalized_new
                feed.title = new_title
                await session.commit()
                await session.refresh(feed)
                return feed
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exception"
                msg += ": Cannot del feed"
            else:
                msg = f"Unexpected Exception ({type(e).__name__})"
            extra = {
                "new_title": new_title,
                "user_id": user_id,
            }
            logger.error(msg, extra=extra)
            raise
