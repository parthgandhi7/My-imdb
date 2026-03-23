import re
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AgentIntent:
    query: str
    years: list[int]
    genres: list[str]
    mood: str | None
    provider: str | None


GENRE_HINTS = {
    "rom-com": "Romance",
    "romcom": "Romance",
    "romantic": "Romance",
    "comedy": "Comedy",
    "horror": "Horror",
    "thriller": "Thriller",
    "bollywood": "Indian",
    "light": "Feel-good",
    "family": "Family",
    "action": "Action",
}


def parse_intent(prompt: str, provider: str | None = None) -> AgentIntent:
    lowered = prompt.lower()

    years = sorted({int(year) for year in re.findall(r"\b(19\d{2}|20\d{2}|21\d{2})\b", prompt)})
    if not years:
        now = datetime.utcnow().year
        if "new" in lowered or "newer" in lowered or "latest" in lowered:
            years = [now - 1, now]

    genres = [genre for hint, genre in GENRE_HINTS.items() if hint in lowered]
    mood = "lighthearted" if "light" in lowered else None

    return AgentIntent(
        query=prompt,
        years=years,
        genres=sorted(set(genres)),
        mood=mood,
        provider=provider.lower() if provider else _extract_provider(lowered),
    )


def _extract_provider(lowered_prompt: str) -> str | None:
    known = ["netflix", "prime video", "amazon prime video", "disney+", "hulu", "max", "apple tv+"]
    for provider in known:
        if provider in lowered_prompt:
            return provider
    return None
