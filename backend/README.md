# Backend (FastAPI)

## Features
- Movie CRUD with watch status and like/dislike sentiment.
- Two list endpoints for **Watchlist** and **History**.
- AI search endpoint that interprets natural language and queries OMDb.
- Excludes watched OMDb/IMDb titles from agent recommendations.

## Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Create `.env` and add:
```env
OMDB_API_KEY=your_omdb_api_key
```

## Run
```bash
uvicorn app.main:app --reload --port 8000
```

## Test
```bash
PYTHONPATH=. pytest
```
