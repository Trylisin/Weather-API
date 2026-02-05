import requests

from .config import ValidationError


def build_cache_key(city: str) -> str:
    return f"weather:{city.lower().strip()}"


def validate_city(city: str) -> str:
    normalized = city.strip()
    if len(normalized) < 2:
        raise ValidationError("City code must be at least 2 characters.")
    return normalized


def fetch_weather(base_url: str, api_key: str, city: str, timeout_seconds: float):
    if not api_key:
        raise ValidationError("Weather API key not configured.")

    url = f"{base_url}/{city}"
    params = {
        "unitGroup": "metric",
        "include": "current",
        "key": api_key,
        "contentType": "json",
    }

    response = requests.get(url, params=params, timeout=timeout_seconds)
    if response.status_code == 404:
        raise ValidationError("City not found.")
    response.raise_for_status()
    return response.json()
