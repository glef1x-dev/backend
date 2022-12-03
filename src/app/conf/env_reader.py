import pathlib

import environ

PATH_TO_ENV_FILE = (pathlib.Path(__file__).parent.parent / ".env").resolve()

env = environ.Env(
    DEBUG=(bool, False),
    CI=(bool, False),
)

environ.Env.read_env(PATH_TO_ENV_FILE)
