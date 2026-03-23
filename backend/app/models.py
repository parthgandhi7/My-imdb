from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class Sentiment(str, Enum):
    liked = "liked"
    disliked = "disliked"
    neutral = "neutral"


class Movie(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    imdb_id: Optional[str] = Field(default=None, index=True)
    title: str = Field(index=True)
    release_year: Optional[int] = Field(default=None, index=True)
    overview: Optional[str] = None
    poster_url: Optional[str] = None
    providers: str = Field(default="")
    watched: bool = Field(default=False, index=True)
    sentiment: Sentiment = Field(default=Sentiment.neutral)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
