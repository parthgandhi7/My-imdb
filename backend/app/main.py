from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from app.db import get_session, init_db
from app.models import Movie, Sentiment
from app.schemas import AgentSearchRequest, AgentSearchResult, MovieCreate, MovieRead, MovieUpdate
from app.services.agent import parse_intent
from app.services.tmdb import TMDBClient, poster_url

app = FastAPI(title="Movie Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _to_movie_read(movie: Movie) -> MovieRead:
    providers = [item.strip() for item in movie.providers.split(",") if item.strip()]
    return MovieRead(
        id=movie.id,
        tmdb_id=movie.tmdb_id,
        title=movie.title,
        release_year=movie.release_year,
        overview=movie.overview,
        poster_url=movie.poster_url,
        providers=providers,
        watched=movie.watched,
        sentiment=movie.sentiment,
    )


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/movies", response_model=list[MovieRead])
def list_movies(session: Session = Depends(get_session)):
    movies = session.exec(select(Movie).order_by(Movie.created_at.desc())).all()
    return [_to_movie_read(movie) for movie in movies]


@app.post("/movies", response_model=MovieRead, status_code=201)
def add_movie(payload: MovieCreate, session: Session = Depends(get_session)):
    movie = Movie(
        title=payload.title.strip(),
        tmdb_id=payload.tmdb_id,
        release_year=payload.release_year,
        overview=payload.overview,
        poster_url=payload.poster_url,
        providers=",".join(sorted(set(payload.providers))),
    )
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return _to_movie_read(movie)


@app.patch("/movies/{movie_id}", response_model=MovieRead)
def update_movie(movie_id: int, payload: MovieUpdate, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    if payload.watched is not None:
        movie.watched = payload.watched
    if payload.sentiment is not None:
        movie.sentiment = payload.sentiment
    if payload.providers is not None:
        movie.providers = ",".join(sorted(set(payload.providers)))

    movie.updated_at = datetime.utcnow()
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return _to_movie_read(movie)


@app.get("/movies/watchlist", response_model=list[MovieRead])
def watchlist(session: Session = Depends(get_session)):
    movies = session.exec(select(Movie).where(Movie.watched.is_(False)).order_by(Movie.created_at.desc())).all()
    return [_to_movie_read(movie) for movie in movies]


@app.get("/movies/history", response_model=list[MovieRead])
def history(session: Session = Depends(get_session)):
    movies = session.exec(select(Movie).where(Movie.watched.is_(True)).order_by(Movie.updated_at.desc())).all()
    return [_to_movie_read(movie) for movie in movies]


@app.post("/agent/search", response_model=list[AgentSearchResult])
async def agent_search(payload: AgentSearchRequest, session: Session = Depends(get_session)):
    client = TMDBClient()
    if not client.is_configured:
        raise HTTPException(status_code=503, detail="TMDB_API_KEY is not configured")

    intent = parse_intent(payload.prompt, provider=payload.provider)
    watched_tmdb_ids = {
        movie.tmdb_id
        for movie in session.exec(select(Movie).where(Movie.watched.is_(True))).all()
        if movie.tmdb_id is not None
    }

    discovered = await client.discover_movies(years=intent.years, limit=payload.limit * 3)
    if not discovered:
        discovered = await client.search_movies(intent.query, limit=payload.limit * 3)

    results: list[AgentSearchResult] = []
    for item in discovered:
        tmdb_id = item.get("id")
        if not tmdb_id or tmdb_id in watched_tmdb_ids:
            continue

        providers = await client.movie_watch_providers(tmdb_id)
        if intent.provider:
            normalized = {p.lower() for p in providers}
            if intent.provider not in normalized:
                continue

        results.append(
            AgentSearchResult(
                tmdb_id=tmdb_id,
                title=item.get("title") or item.get("name") or "Unknown",
                release_date=item.get("release_date"),
                overview=item.get("overview"),
                poster_url=poster_url(item.get("poster_path")),
                genres=intent.genres,
                providers=providers,
            )
        )
        if len(results) >= payload.limit:
            break

    return results


@app.post("/movies/{movie_id}/toggle-watched", response_model=MovieRead)
def toggle_watched(movie_id: int, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie.watched = not movie.watched
    movie.updated_at = datetime.utcnow()
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return _to_movie_read(movie)


@app.post("/movies/{movie_id}/like", response_model=MovieRead)
def like_movie(movie_id: int, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie.sentiment = Sentiment.liked
    movie.updated_at = datetime.utcnow()
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return _to_movie_read(movie)


@app.post("/movies/{movie_id}/dislike", response_model=MovieRead)
def dislike_movie(movie_id: int, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie.sentiment = Sentiment.disliked
    movie.updated_at = datetime.utcnow()
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return _to_movie_read(movie)
