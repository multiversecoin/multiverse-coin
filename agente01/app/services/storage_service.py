"""MinIO/S3 storage service for secure evidence management."""

import io
import uuid
from typing import BinaryIO, Optional

from minio import Minio
from minio.error import S3Error

from app.core.config import settings

_client: Optional[Minio] = None


def get_minio_client() -> Minio:
    global _client
    if _client is None:
        _client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_USE_SSL,
        )
    return _client


def ensure_bucket():
    client = get_minio_client()
    if not client.bucket_exists(settings.MINIO_BUCKET):
        client.make_bucket(settings.MINIO_BUCKET)


def upload_file(
    file_data: BinaryIO,
    storage_key: str,
    content_type: str = "application/octet-stream",
    file_size: int = -1,
) -> str:
    client = get_minio_client()
    ensure_bucket()

    if file_size < 0:
        file_data.seek(0, 2)
        file_size = file_data.tell()
        file_data.seek(0)

    client.put_object(
        settings.MINIO_BUCKET,
        storage_key,
        file_data,
        length=file_size,
        content_type=content_type,
    )
    return storage_key


def download_file(storage_key: str) -> bytes:
    client = get_minio_client()
    response = client.get_object(settings.MINIO_BUCKET, storage_key)
    data = response.read()
    response.close()
    response.release_conn()
    return data


def generate_presigned_url(storage_key: str, expires_hours: int = 1) -> str:
    from datetime import timedelta

    client = get_minio_client()
    return client.presigned_get_object(
        settings.MINIO_BUCKET,
        storage_key,
        expires=timedelta(hours=expires_hours),
    )


def delete_file(storage_key: str):
    client = get_minio_client()
    client.remove_object(settings.MINIO_BUCKET, storage_key)


def generate_storage_key(operation_id: str, filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1] if "." in filename else "bin"
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    return f"operations/{operation_id}/evidences/{unique_name}"


def generate_report_storage_key(operation_id: str, fmt: str) -> str:
    return f"operations/{operation_id}/reports/{uuid.uuid4().hex}.{fmt}"
