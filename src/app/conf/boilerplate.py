import pathlib

from app.conf.env_reader import env

BASE_DIR = pathlib.Path(__file__).parent.parent.resolve()

ROOT_URLCONF = 'app.urls'

# Disable built-in ./manage.py test command in favor of pytest
TEST_RUNNER = 'app.test.disable_test_command_runner.DisableTestCommandRunner'

WSGI_APPLICATION = 'app.wsgi.application'

DEBUG = env('DEBUG', cast=bool, default=False)

try:
    import orjson as json

    JSON_SERIALIZER = json.dumps
except ImportError:
    import json

    JSON_SERIALIZER = json.dumps
