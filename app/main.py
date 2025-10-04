from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from app.User.router import router as router_users
from app.Article.router import router as router_articles
from app.Feed.router import router as router_feeds
from app.User.models import User
from app.Article.models import Article
from app.Feed.models import Feed
from fastapi_cache.backends.redis import RedisBackend
from app.config import settings
from redis import asyncio as aioredis

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=False,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    await redis.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router_users)
app.include_router(router_articles)
app.include_router(router_feeds)

@app.get("/")
async def init_fastapi():
    return {"FastAPI" : "Success"}
