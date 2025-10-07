import pytest
from sqlalchemy import select

from app.Article.dao import ArticleDAO
from app.Article.models import Article
from app.exceptions import NoArticle
from app.database import async_session

@pytest.mark.parametrize(
    "user_id,is_present",
    [
        (1,True),
        (2,True),
        (10,False)
    ],
)
async def test_get_your_article_by_user(user_id,is_present):
    if is_present:
        article = await ArticleDAO.get_your_article_by_user(user_id)
        assert article is not None
    else:
        with pytest.raises(NoArticle):
            await ArticleDAO.get_your_article_by_user(user_id)
            
@pytest.mark.parametrize(
    "article_id,user_id,is_present",
    [
        (1,1,True),
        (2,1,True),
        (10,10,False)
    ],
)
async def test_delete_your_article(article_id,user_id,is_present):
    delete_feed = await ArticleDAO.delete_your_article_by_id(article_id, user_id)
    if is_present:
        assert delete_feed > 0
    else:
        assert delete_feed == 0
        
@pytest.mark.parametrize(
    "user_id,tag,is_present",
    [
        (1,"ai",True),
        (2,"climate",True),
        (10,"dsadasdsa",False)
    ],
)           
async def test_get_article_by_tag(user_id, tag, is_present):    #TODO Я ЧЕСТНО НЕ ЗНАЮ ПОЧЕМУ ОН БЕРЕТ ТОЛЬКО ОДНУ СТАТЬЮ И ТУ ВЫБИРАЕТ СЛУЧАЙНО
    if is_present:
        articles = await ArticleDAO.get_articles_by_tag(user_id, tag)
        print(articles)
        assert len(articles) >= 1
        for article in articles:
            assert article.feed.user_id == user_id
            assert tag in article.tags
    else:
        with pytest.raises(NoArticle):
            await ArticleDAO.get_articles_by_tag(user_id, tag)