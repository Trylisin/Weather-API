# Weather Cache API + UI

A production-ready Flask API with Redis caching and a Vue UI. The API proxies Visual Crossing and caches responses for 12 hours by default.

## Quick start

1. Create `.env` from `.env.example` and add your API key.
2. Run:

```bash
docker compose up --build
```

- UI: http://localhost:8080
- API: http://localhost:8000

## Endpoints

- `GET /health`
- `GET /weather?city=Berlin`

## Notes

- Cache key uses the user-provided city code in lowercase.
- Redis TTL defaults to 12 hours (`43200` seconds).
- Rate limit defaults to 60 requests per minute per IP.
