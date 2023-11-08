import os
import boto3
from botocore.client import Config


def required_env(name):
    value = os.getenv(name)
    if value is None:
        raise Exception(f"Environment variable {name} is required")
    return value



s3 = boto3.resource("s3",
                    endpoint_url=required_env('S3_URL'),
                    aws_access_key_id='F1dwh991Xepkq5TZhZxI',
                    aws_secret_access_key=required_env("MINIO_SECRET_KEY"),
                    config=Config(signature_version='s3v4'))

SECRET_KEY = required_env("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
DB_URL = required_env("DB_URL")
