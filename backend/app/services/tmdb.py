import os
from typing import Any

import httpx

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"


class TMDBClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("TMDB_API_KEY")

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)

    async def discover_movies(self, *, years: list[int] | None = None, limit: int = 10) -> list[dict[str, Any]]:
        if not self.api_key:
            return []

        params: dict[str, Any] = {
            "api_key": self.api_key,
            "sort_by": "popularity.desc",
            "include_adult": "false",
            "vote_count.gte": 80,
            "page": 1,
        }
        if years:
            params["primary_release_date.gte"] = f"{min(years)}-01-01"
            params["primary_release_date.lte"] = f"{max(years)}-12-31"

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(f"{TMDB_BASE_URL}/discover/movie", params=params)
            resp.raise_for_status()
            payload = resp.json()
        return payload.get("results", [])[:limit]

    async def search_movies(self, query: str, *, limit: int = 10) -> list[dict[str, Any]]:
        if not self.api_key:
            return []

        params = {"api_key": self.api_key, "query": query, "include_adult": "false", "page": 1}
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(f"{TMDB_BASE_URL}/search/movie", params=params)
            resp.raise_for_status()
            payload = resp.json()
        return payload.get("results", [])[:limit]

    async def movie_watch_providers(self, movie_id: int, country_code: str = "US") -> list[str]:
        if not self.api_key:
            return []

        params = {"api_key": self.api_key}
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(f"{TMDB_BASE_URL}/movie/{movie_id}/watch/providers", params=params)
            resp.raise_for_status()
            payload = resp.json()

        country = payload.get("results", {}).get(country_code, {})
        flatrate = country.get("flatrate", [])
        return sorted({item["provider_name"] for item in flatrate if item.get("provider_name")})


def poster_url(path: str | None) -> str | None:
    if not path:
        return None
    return f"{TMDB_IMAGE_BASE}{path}"
