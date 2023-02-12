from app.conf.env_reader import env

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env.str("REDIS_URL", "redis://127.0.0.1:6379"),
    }
}

DEFAULT_CACHE_TIME = 60 * 5  # 5 minutes
