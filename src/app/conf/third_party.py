import warnings

from app.conf.env_reader import env

GITHUB_API_TOKEN = env.str("GITHUB_API_TOKEN", default=None)

if not GITHUB_API_TOKEN and not env("DEBUG", default=True):
    warnings.warn(
        "GITHUB_API_TOKEN environment variable was not provided. Application is going to use github API without the token. "  # noqa: E501
        "It can cause throttling of requests. Visit https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token."  # noqa: E501
    )

if env("DEBUG", cast=bool, default=True):
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]
