from fastapi import APIRouter, Depends
from pydantic import HttpUrl

from app.Feed.dao import FeedDAO
from app.Feed.schemas import SFeed, SFeedResponse
from app.User.dependencies import get_current_user
from app.User.models import User

router = APIRouter(prefix="/feed", tags=["Лента новостей"])


@router.post("", response_model=SFeedResponse)
async def add_rss(
    feed_data: SFeed, current_user: User = Depends(get_current_user)
):
    new_feed = await FeedDAO.add_feed(
        current_user.id, feed_data.url, feed_data.title
    )
    return SFeedResponse(
        id=new_feed.id,
        url=new_feed.url,
        title=new_feed.title,
        is_active=new_feed.is_active,
    )


@router.get("/all")
async def get_rss(current_user=Depends(get_current_user)):
    return await FeedDAO.find_all(user_id=current_user.id)


@router.delete("/delete")
async def delete_rss(
    feed_id: int, current_user: User = Depends(get_current_user)
):
    delete_feed = await FeedDAO.delete_feed(feed_id, current_user.id)
    if delete_feed == True:
        return {"Ссылка удалена"}
    else:
        return {"Ссылки не существует"}


@router.put("/edit")
async def update_rss(
    Feed: SFeed, url: HttpUrl, current_user: User = Depends(get_current_user)
):
    new_feed = await FeedDAO.update_feed(
        current_user.id, url, Feed.title, Feed.url
    )
    return SFeedResponse(
        id=new_feed.id,
        url=new_feed.url,
        title=new_feed.title,
        is_active=new_feed.is_active,
    )
