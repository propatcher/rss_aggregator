# app/tasks.py
from celery import shared_task
from sqlalchemy.orm import Session
from app.database import sync_session
from app.User.models import User
from app.Feed.models import Feed
from app.Article.models import Article
from app.Feed.parser import parse_rss_feed

def get_db():
    db = sync_session()
    try:
        yield db
    finally:
        db.close()

@shared_task
def sync_all_feeds():
    db: Session = next(get_db())
    try:
        feeds = db.query(Feed).filter(Feed.is_active == True).all()
        print(f"Найдено активных лент: {len(feeds)}")

        for feed in feeds:
            print(f"Парсинг ленты: {feed.url}")
            articles_data = parse_rss_feed(feed.url)

            for data in articles_data:
                existing = db.query(Article).filter(
                    Article.feed_id == feed.id,
                    Article.link == data["link"]
                ).first()

                if not existing:
                    new_article = Article(
                        feed_id=feed.id,
                        title=data["title"],
                        summary=data["summary"],
                        link=data["link"],
                        published_at=data["published_at"],
                        tags=data["tags"],
                        is_read=False
                    )
                    db.add(new_article)
                    print(f"Добавлена новая статья: {data['title'][:50]}...")

            db.commit()

    except Exception as e:
        db.rollback()
        print(f"Ошибка в sync_all_feeds: {e}")
    finally:
        db.close()