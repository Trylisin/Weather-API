# Weather Cache API + UI

A weather service:
- Flask API that fetches Visual Crossing data
- Redis caching to keep responses fast
- Vue UI for quick lookups
- Docker Compose to run everything with one command

## Quick Start

1. Copy `.env.example` to `.env` and add your Visual Crossing key.
2. Build and run the stack:

```bash
docker compose up --build
```

Open:
- UI: http://localhost:8080
- API: http://localhost:8000

## What You Get

- `GET /health` for a simple health check
- `GET /weather?city=Berlin` for live + cached weather

## How Caching Works

- Cache key: `weather:{city}` (lowercased)
- Default TTL: 12 hours (`43200` seconds)
- Rate limit: 60 requests per minute per IP

## Tips

- Try a few cities in the UI to see cache vs live responses.
- If Redis is unavailable, the API will still return live data.
