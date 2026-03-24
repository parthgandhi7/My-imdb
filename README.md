# Movie Tracker App (Python + React)

A mobile-friendly movie tracker with:
- **Watchlist** and **History** tabs.
- Per-movie controls: **Watched/Unwatched**, **Like/Dislike**.
- AI-powered natural-language movie discovery using **OMDb**.

## Tech Stack
- **Backend:** FastAPI + SQLModel + SQLite
- **Frontend:** React + Vite
- **Movie data:** OMDb API

## Project Structure
- `backend/` - API, DB models, AI agent logic, OMDb integration
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
# set OMDB_API_KEY in .env
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
2. Fetches candidates from OMDb search.
3. Excludes already watched movies from local DB history.

## Docs
- Backend docs: `backend/README.md`
- Frontend docs: `frontend/README.md`
- Deployment docs: `DEPLOYMENT.md`

## GitHub Actions + Vercel Deployment
This repository now includes `.github/workflows/vercel.yml` to automatically:
- Run frontend build checks on every PR to `main` and every push to `main`.
- Deploy **Preview** builds for pull requests.
- Deploy **Production** builds for pushes to `main`.

### Required GitHub secrets
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`

### Required Vercel environment variable
Set this in your Vercel project so the frontend can talk to the API:
- `VITE_API_BASE_URL` (for example, your deployed backend URL)

### Where to find the deployed URL
After the workflow runs, open the workflow run in GitHub Actions and check the **job summary** for:
- `Preview deployment URL: ...` (for PRs)
- `Production deployment URL: ...` (for pushes to `main`)

### If you see `react-scripts build exited with 127` on Vercel
That means Vercel is using old Create React App build settings. This repo uses **Vite**.
- `vercel.json` (repo root) now forces build from `frontend/`.
- `frontend/vercel.json` also enforces Vite settings when the Vercel project root is set to `frontend`.

After pulling latest code, trigger a redeploy.
