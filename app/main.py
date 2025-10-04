from contextlib import asynccontextmanager
import time
from fastapi import FastAPI, Request
from fastapi_cache import FastAPICache
from prometheus_fastapi_instrumentator import Instrumentator
from app.User.router import router as router_users
from app.Article.router import router as router_articles
from app.Feed.router import router as router_feeds
from app.User.models import User
from app.Article.models import Article
from fastapi.middleware.cors import CORSMiddleware
from app.Feed.models import Feed
from fastapi_cache.backends.redis import RedisBackend
from app.admin.admin_setup import setup_admin
from app.config import settings
from redis import asyncio as aioredis
from app.logger import logger
from app.database import engine

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

admin = setup_admin(app, engine)

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
instrumentator.instrument(app).expose(app)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://test",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def init_fastapi():
    return {"FastAPI" : "Success"}

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info("Request exec time", extra={
        "procces_time" : round(process_time,4)
    })
    return response
