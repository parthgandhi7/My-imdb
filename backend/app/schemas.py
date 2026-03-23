from typing import Optional

from pydantic import BaseModel, Field

from app.models import Sentiment


class MovieCreate(BaseModel):
    title: str = Field(min_length=1)
    tmdb_id: Optional[int] = None
    release_year: Optional[int] = None
    overview: Optional[str] = None
    poster_url: Optional[str] = None
    providers: list[str] = Field(default_factory=list)


class MovieUpdate(BaseModel):
    watched: Optional[bool] = None
    sentiment: Optional[Sentiment] = None
    providers: Optional[list[str]] = None


class MovieRead(BaseModel):
    id: int
    tmdb_id: Optional[int]
    title: str
    release_year: Optional[int]
    overview: Optional[str]
    poster_url: Optional[str]
    providers: list[str]
    watched: bool
    sentiment: Sentiment


class AgentSearchRequest(BaseModel):
    prompt: str = Field(min_length=3)
    provider: Optional[str] = None
    limit: int = Field(default=10, ge=1, le=20)


class AgentSearchResult(BaseModel):
    tmdb_id: int
    title: str
    release_date: Optional[str]
    overview: Optional[str]
    poster_url: Optional[str]
    genres: list[str]
    providers: list[str]
