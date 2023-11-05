import os

def required_env(name):
    value = os.getenv(name)
    if value is None:
        raise Exception(f"Environment variable {name} is required")
    return value


SECRET_KEY = required_env("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
DB_URL = required_env("DB_URL")