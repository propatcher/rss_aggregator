from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, HttpUrl


class SArticle(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    summary: Optional[str] = None
    link: HttpUrl
    published_at: datetime
    is_read: bool
    tags: Optional[Any] = None
    created_at: datetime


class SArticleResponse(SArticle):
    id: int
