import os

from dotenv import load_dotenv

load_dotenv()


class Connection:
    DATABASE_URL = os.getenv("POSTGRES_URL")
    DATABASE = os.getenv("DATABASE")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")


class S3Connection:
    ACCESS_KEY = os.getenv("ACCESS_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")
    BUCKET_NAME = os.getenv("BUCKET_NAME")


if __name__ == '__main__':
    print(f"""
Database_URL = {Connection.DATABASE_URL}
DATABSE = {Connection.DATABASE}
    """)
