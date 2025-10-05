import pytest

from app.Feed.dao import FeedDAO
from app.exceptions import FeedNotFound, InvalidRssLink

@pytest.mark.parametrize(
    "user_id,url,title,is_present",
    [
        (1,"https://habr.com/ru/rss/articles/","Habr",True),
        (2,"sdsssddsadsadasdasdsadadad","asasa",False)
    ],
)
async def test_add_rss(user_id, url, title, is_present):
    if is_present:
        new_feed = await FeedDAO.add_feed(user_id, url, title)
        assert new_feed is not None
        assert new_feed.title == title
    else:
        with pytest.raises(InvalidRssLink):
            await FeedDAO.add_feed(user_id, url, title)
            
@pytest.mark.parametrize(
    "feed_id,user_id,is_present",
    [
        (1,1,True),
        (2,1,True),
        (2,2,False)
    ],
)
async def test_delete_rss(feed_id,user_id,is_present):
    delete_feed = await FeedDAO.delete_feed(feed_id, user_id)
    if is_present:
        assert delete_feed == True
    else:
        assert delete_feed == False

@pytest.mark.parametrize(
    "user_id,old_url,new_title,new_url,is_present",
    [
        (2,"https://rss.cnn.com/rss/edition.rss","Test","https://habr.com/ru/rss/articles/",True),
        (2,"https://techblog.example.com/feed.xml","Test","https://habr.com/ru/rss/articles/",False),
    ],  
)
async def test_update_rss(user_id,old_url,new_title,new_url,is_present):
    if is_present:
        new_feed = await FeedDAO.update_feed(
            user_id, old_url, new_title, new_url
        )
        assert new_feed.title == new_title
        assert new_feed.url == new_url
    else:
        with pytest.raises(FeedNotFound):
            await FeedDAO.update_feed(user_id, old_url, new_title, new_url)