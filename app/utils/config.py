import os

from dotenv import load_dotenv

load_dotenv()


class Connection:
    DATABASE_URL = os.getenv("POSTGRES_URL")
    DATABASE = os.getenv("DATABASE")


class S3Connection:
    ACCESS_KEY = os.getenv("ACCESS_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")
    BUCKET_NAME = os.getenv("BUCKET_NAME")
