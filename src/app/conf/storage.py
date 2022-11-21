from django.conf import settings

from app.conf.env_reader import env

DEFAULT_FILE_STORAGE = env('DEFAULT_FILE_STORAGE', cast=str, default='django.core.files.storage.FileSystemStorage')

if not settings.DEBUG:
    AWS_ACCESS_KEY_ID = env('S3_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('S3_SECRET_ACCESS_KEY')
    AWS_S3_REGION_NAME = env('S3_REGION_NAME')
    AWS_STORAGE_BUCKET_NAME = env('S3_BUCKET_NAME')
    AWS_S3_ENDPOINT_URL = f"https://glefixmedia.{AWS_S3_REGION_NAME}.digitaloceanspaces.com"
    AWS_DEFAULT_ACL = env('S3_DEFAULT_ACL', default='public-read')
    AWS_IS_GZIPPED = env('S3_IS_GZIPPED', default=False)
    AWS_QUERYSTRING_AUTH = env('S3_QUERYSTRING_AUTH', default=True)

    # It's should be like https://${S3_CUSTOM_DOMAIN}/${AWS_STORAGE_BUCKET_NAME} or something like that
    AWS_S3_CUSTOM_DOMAIN = env('S3_CUSTOM_DOMAIN', cast=str) + f"/{AWS_STORAGE_BUCKET_NAME}"

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
