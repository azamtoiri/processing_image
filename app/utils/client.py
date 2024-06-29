from app.utils.config import S3Connection
from app.utils.s3_client import S3Client


def get_s3_client() -> S3Client:
    return S3Client(
        access_key=S3Connection.ACCESS_KEY,
        secret_key=S3Connection.SECRET_KEY,
        bucket_name=S3Connection.BUCKET_NAME
    )
