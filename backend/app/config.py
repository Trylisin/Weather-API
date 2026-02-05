import os


def get_env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return value


def build_config() -> dict:
    cache_url = get_env("REDIS_URL", "redis://redis:6379/0")
    return {
        "ENV": get_env("FLASK_ENV", "production"),
        "API_KEY": get_env("WEATHER_API_KEY"),
        "API_BASE_URL": get_env(
            "WEATHER_API_BASE_URL",
            "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline",
        ),
        "CACHE_URL": cache_url,
        "CACHE_TTL_SECONDS": int(get_env("CACHE_TTL_SECONDS", "43200")),
        "RATE_LIMIT": get_env("RATE_LIMIT", "60 per minute"),
        "RATE_LIMIT_STORAGE_URL": get_env("RATE_LIMIT_STORAGE_URL", cache_url),
        "REQUEST_TIMEOUT_SECONDS": float(get_env("REQUEST_TIMEOUT_SECONDS", "8")),
    }


class ValidationError(Exception):
    pass
