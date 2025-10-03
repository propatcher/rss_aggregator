from fastapi import FastAPI
from app.User.router import router as router_users
from app.Article.router import router as router_articles
from app.Feed.router import router as router_feeds
from app.User.models import User
from app.Article.models import Article
from app.Feed.models import Feed

app = FastAPI()

app.include_router(router_users)
app.include_router(router_articles)
app.include_router(router_feeds)

@app.get("/")
async def init_fastapi():
    return {"FastAPI" : "Success"}
