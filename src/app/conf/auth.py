from datetime import timedelta

from app.conf.env_reader import env

AUTH_USER_MODEL = "users.User"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
]

AXES_ENABLED = env("AXES_ENABLED", cast=bool, default=True)
AXES_FAILURE_LIMIT = 10
AXES_META_PRECEDENCE_ORDER = [
    "HTTP_X_FORWARDED_FOR",
    "REMOTE_ADDR",
]
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True
# Fifteen minutes
AXES_COOLOFF_TIME = 0.15

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesBackend",
    "django.contrib.auth.backends.ModelBackend",
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=2),
    "ALGORITHM": "HS512",
    "UPDATE_LAST_LOGIN": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ROTATE_REFRESH_TOKENS": True,
}

DEBUG = env("DEBUG", cast=bool, default=False)

if DEBUG:
    SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(days=1)

REFRESH_TOKEN_COOKIE_NAME = env.str("REFRESH_TOKEN_COOKIE_NAME", "refresh")
