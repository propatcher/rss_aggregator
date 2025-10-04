from celery import Celery

celery = Celery(
    "rss_aggregator",
    broker="redis://localhost:6379",
    backend="redis://localhost:6379",
    include=["app.tasks.tasks"]
)

celery.conf.beat_schedule = {
    "sync-all-feeds-hourly": {
        "task": "app.tasks.tasks.sync_all_feeds",
        "schedule": 3600,
    },
}

celery.conf.timezone = "UTC"