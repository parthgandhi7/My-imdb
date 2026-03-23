# Deployment Guide

## 1) Backend Deployment (Render/Railway/Fly.io)
1. Create a Python web service from `/backend`.
2. Install command:
   ```bash
   pip install -r requirements.txt
   ```
3. Start command:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
4. Add environment variable `OMDB_API_KEY`.
5. Persist `/workspace/My-imdb/data` (or map a volume) for SQLite data durability.

## 2) Frontend Deployment (Vercel/Netlify)
1. Deploy `/frontend` as a static app.
2. Build command:
   ```bash
   npm run build
   ```
3. Output directory: `dist`.
4. Add `VITE_API_BASE_URL` to point to backend URL.

## 3) CI/CD secret management (recommended)
Use CI/CD secrets instead of committing keys in files.

### GitHub Actions
1. Go to **Settings → Secrets and variables → Actions**.
2. Add a repository secret named `OMDB_API_KEY`.
3. Inject it into deploy jobs with:
   ```yaml
   env:
     OMDB_API_KEY: ${{ secrets.OMDB_API_KEY }}
   ```

### Render / Railway / Fly.io
- Set `OMDB_API_KEY` in the platform's environment variables or secret manager.
- Never hardcode the key in source-controlled files.

## 4) Docker Compose (local/self-host)
Use this sample `docker-compose.yml`:

```yaml
version: "3.9"
services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - OMDB_API_KEY=${OMDB_API_KEY}
    volumes:
      - ./data:/app/data

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "5173:4173"
    environment:
      - VITE_API_BASE_URL=http://backend:8000
    depends_on:
      - backend
```

You can also deploy frontend and backend independently for easier scaling.
