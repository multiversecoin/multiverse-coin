"""SHA-256 hashing for evidence integrity verification."""

import hashlib
from pathlib import Path
from typing import BinaryIO


HASH_ALGORITHM = "sha256"
CHUNK_SIZE = 8192


def compute_sha256(file_obj: BinaryIO) -> str:
    hasher = hashlib.sha256()
    file_obj.seek(0)
    while chunk := file_obj.read(CHUNK_SIZE):
        hasher.update(chunk)
    file_obj.seek(0)
    return hasher.hexdigest()


def compute_sha256_from_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compute_sha256_from_path(path: str) -> str:
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            hasher.update(chunk)
    return hasher.hexdigest()


def verify_integrity(file_obj: BinaryIO, expected_hash: str) -> bool:
    computed = compute_sha256(file_obj)
    return computed == expected_hash
