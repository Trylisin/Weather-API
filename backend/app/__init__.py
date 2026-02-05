from flask import Flask, jsonify
from flask_limiter.errors import RateLimitExceeded
from dotenv import load_dotenv

from .cache import get_redis
from .config import build_config
from .limiter import create_limiter
from .routes import bp


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.update(build_config())

    limiter = create_limiter(app.config["RATE_LIMIT"], app.config["RATE_LIMIT_STORAGE_URL"])
    limiter.init_app(app)

    bp.config = app.config
    bp.redis = get_redis(app.config["CACHE_URL"])
    app.register_blueprint(bp)

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(RateLimitExceeded)
    def rate_limited(_):
        return jsonify({"error": "Rate limit exceeded. Try again later."}), 429

    return app
