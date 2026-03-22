# Movie Tracker App (Python + React)

A mobile-friendly movie tracker with:
- **Watchlist** and **History** tabs.
- Per-movie controls: **Watched/Unwatched**, **Like/Dislike**.
- OTT provider visibility per movie.
- AI-powered natural-language movie discovery using **TMDB** (with provider-specific filtering such as Netflix-only).

## Tech Stack
- **Backend:** FastAPI + SQLModel + SQLite
- **Frontend:** React + Vite
- **Movie data:** TMDB API

## Project Structure
- `backend/` - API, DB models, AI agent logic, TMDB integration
- `frontend/` - React UI
- `DEPLOYMENT.md` - deployment options and Docker guidance

## Quick Start
### 1) Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# set TMDB_API_KEY in .env
uvicorn app.main:app --reload --port 8000
```

### 2) Frontend
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## AI Agent Behavior
Given input like:
- "A light Bollywood rom-com from 2025"
- "I want a light movie like Stree but newer"

The app:
1. Parses user intent (vibe, years, genre hints, provider hints).
2. Fetches candidates from TMDB discover/search.
3. Filters by selected/parsed OTT provider (e.g., Netflix).
4. Excludes already watched movies from local DB history.

## Docs
- Backend docs: `backend/README.md`
- Frontend docs: `frontend/README.md`
- Deployment docs: `DEPLOYMENT.md`
