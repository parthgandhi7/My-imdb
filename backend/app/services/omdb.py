import os
from typing import Any

import httpx

OMDB_BASE_URL = "https://www.omdbapi.com/"


class OMDBClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("OMDB_API_KEY")

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)

    async def discover_movies(self, *, years: list[int] | None = None, limit: int = 10) -> list[dict[str, Any]]:
        """
        OMDb has no true discover endpoint, so use broad title searches and optionally
        filter by year range.
        """
        query = "movie"
        if years:
            year = max(years)
            return await self.search_movies(query, year=year, limit=limit)

        return await self.search_movies(query, limit=limit)

    async def search_movies(self, query: str, *, year: int | None = None, limit: int = 10) -> list[dict[str, Any]]:
        if not self.api_key:
            return []

        search_params: dict[str, Any] = {"apikey": self.api_key, "s": query or "movie", "type": "movie"}
        if year:
            search_params["y"] = year

        async with httpx.AsyncClient(timeout=20.0) as client:
            search_resp = await client.get(OMDB_BASE_URL, params=search_params)
            search_resp.raise_for_status()
            search_payload = search_resp.json()

            if search_payload.get("Response") != "True":
                return []

            items = search_payload.get("Search", [])[:limit]

            detailed: list[dict[str, Any]] = []
            for item in items:
                imdb_id = item.get("imdbID")
                if not imdb_id:
                    continue
                detail_resp = await client.get(
                    OMDB_BASE_URL,
                    params={"apikey": self.api_key, "i": imdb_id, "plot": "short", "r": "json"},
                )
                detail_resp.raise_for_status()
                detail_payload = detail_resp.json()
                if detail_payload.get("Response") == "True":
                    detailed.append(detail_payload)

        return detailed

    async def movie_watch_providers(self, movie_id: str, country_code: str = "US") -> list[str]:
        """
        OMDb does not provide streaming provider data.
        Kept for compatibility with existing API response shape.
        """
        _ = movie_id, country_code
        return []


def poster_url(path: str | None) -> str | None:
    if not path or path == "N/A":
        return None
    return path
