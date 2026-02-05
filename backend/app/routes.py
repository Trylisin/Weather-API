from flask import Blueprint, jsonify, request

from .cache import cache_get, cache_set
from .config import ValidationError
from .weather import build_cache_key, fetch_weather, validate_city


bp = Blueprint("api", __name__)


@bp.get("/health")
def health():
    return jsonify({"status": "ok"})


@bp.get("/weather")
def weather():
    city = request.args.get("city", "")

    try:
        city = validate_city(city)
    except ValidationError as exc:
        return jsonify({"error": str(exc)}), 400

    cache = bp.redis
    key = build_cache_key(city)
    try:
        cached = cache_get(cache, key)
    except Exception:
        cached = None

    if cached is not None:
        return jsonify({"source": "cache", "data": cached})

    try:
        data = fetch_weather(
            base_url=bp.config["API_BASE_URL"],
            api_key=bp.config["API_KEY"],
            city=city,
            timeout_seconds=bp.config["REQUEST_TIMEOUT_SECONDS"],
        )
    except ValidationError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "Failed to reach weather provider."}), 502

    try:
        cache_set(cache, key, data, bp.config["CACHE_TTL_SECONDS"])
    except Exception:
        pass
    return jsonify({"source": "live", "data": data})
