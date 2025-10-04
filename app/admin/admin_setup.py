from sqladmin import Admin, ModelView

from app.Article.models import Article
from app.Feed.models import Feed
from app.User.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email]
    form_excluded_columns = [User.hashed_password]


class FeedAdmin(ModelView, model=Feed):
    column_list = [
        Feed.id,
        Feed.user_id,
        Feed.url,
        Feed.normalized_url,
        Feed.title,
        Feed.is_active,
    ]


class ArticleAdmin(ModelView, model=Article):
    column_list = [
        Article.id,
        Article.feed_id,
        Article.title,
        Article.summary,
        Article.link,
        Article.published_at,
        Article.is_read,
        Article.tags,
        Article.created_at,
    ]


def setup_admin(app, engine):
    admin = Admin(app, engine)

    admin.add_view(UserAdmin)
    admin.add_view(FeedAdmin)
    admin.add_view(ArticleAdmin)

    return admin
