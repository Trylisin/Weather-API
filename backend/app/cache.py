import json
from redis import Redis


def get_redis(url: str) -> Redis:
    return Redis.from_url(url, decode_responses=True)


def cache_get(redis_client: Redis, key: str):
    cached = redis_client.get(key)
    if cached is None:
        return None
    return json.loads(cached)


def cache_set(redis_client: Redis, key: str, value, ttl_seconds: int) -> None:
    redis_client.set(name=key, value=json.dumps(value), ex=ttl_seconds)
