"""Tests for SHA-256 hashing module."""

import io

from app.core.hashing import compute_sha256, compute_sha256_from_bytes, verify_integrity


def test_sha256_deterministic():
    data = b"test data for hashing"
    hash1 = compute_sha256_from_bytes(data)
    hash2 = compute_sha256_from_bytes(data)
    assert hash1 == hash2
    assert len(hash1) == 64


def test_sha256_file_object():
    data = b"file content for testing"
    file_obj = io.BytesIO(data)
    hash1 = compute_sha256(file_obj)
    hash2 = compute_sha256_from_bytes(data)
    assert hash1 == hash2


def test_verify_integrity():
    data = b"integrity check data"
    file_obj = io.BytesIO(data)
    expected = compute_sha256_from_bytes(data)
    assert verify_integrity(file_obj, expected) is True
    assert verify_integrity(file_obj, "wrong_hash") is False


def test_different_data_different_hash():
    hash1 = compute_sha256_from_bytes(b"data1")
    hash2 = compute_sha256_from_bytes(b"data2")
    assert hash1 != hash2
