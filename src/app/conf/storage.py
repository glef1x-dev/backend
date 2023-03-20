from app.conf.env_reader import env

DEFAULT_FILE_STORAGE = env(
    "DEFAULT_FILE_STORAGE",
    cast=str,
    default="django.core.files.storage.FileSystemStorage",
)

if not env("DEBUG", default=True):
    AWS_ACCESS_KEY_ID = env("S3_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("S3_SECRET_ACCESS_KEY")
    AWS_S3_REGION_NAME = env("S3_REGION_NAME")
    AWS_STORAGE_BUCKET_NAME = env("S3_BUCKET_NAME")
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
