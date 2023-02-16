import warnings

from app.conf.env_reader import env

# Sentry
# https://sentry.io/for/django/

SENTRY_DSN = env("SENTRY_DSN", cast=str, default=None)


if not env("DEBUG") and SENTRY_DSN is not None:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        attach_stacktrace=True,
        send_default_pii=True,
    )
elif not env("DEBUG"):
    warnings.warn(
        "Sentry dsn environment variable is not set."
        "Application is starting without sentry sdk installed in production!"
    )
