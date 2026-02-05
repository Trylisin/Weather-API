from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def create_limiter(default_limits: str, storage_uri: str):
    return Limiter(
        get_remote_address,
        default_limits=[default_limits],
        storage_uri=storage_uri,
    )
