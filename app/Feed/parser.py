from datetime import datetime, timezone
from typing import Dict, List

import feedparser


def parse_rss_feed(url: str):
    try:
        feed = feedparser.parse(url)
        articles = []

        for entry in feed.entries:
            published_at = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published_at = datetime(
                    *entry.published_parsed[:6], tzinfo=timezone.utc
                )
            else:
                published_at = datetime.now(timezone.utc)

            tags = []
            if hasattr(entry, "tags"):
                tags = [
                    tag.term.lower().strip() for tag in entry.tags if tag.term
                ]

            articles.append(
                {
                    "title": entry.get("title", "Без заголовка")[:200],
                    "summary": entry.get("summary", "")[:1000],
                    "link": entry.get("link", ""),
                    "published_at": published_at,
                    "tags": tags or None,
                }
            )

        return articles

    except Exception as e:
        print(f"Ошибка при парсинге {url}: {e}")
        return []
