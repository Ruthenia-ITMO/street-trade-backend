import os
import aioboto3
from botocore.client import Config


def required_env(name):
    value = os.getenv(name)
    if value is None:
        raise Exception(f"Environment variable {name} is required")
    return value


RTSPTOWEB_URL = required_env("RTSPTOWEB_URL")
S3_URL = required_env("S3_URL")
S3_ACCESS_KEY = required_env("S3_ACCESS_KEY")
S3_SECRET_ACCESS_KEY = required_env("S3_SECRET_ACCESS_KEY")
S3_BUCKET = required_env("S3_BUCKET")
SECRET_KEY = required_env("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
DB_URL = required_env("DB_URL")
ADMIN_PASSWORD = required_env("ADMIN_PASSWORD")
