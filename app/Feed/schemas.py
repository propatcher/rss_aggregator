from pydantic import BaseModel, ConfigDict, HttpUrl


class SFeed(BaseModel):
    url: str
    title: str


class SFeedResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: HttpUrl
    title: str
    is_active: bool
