"""Tests for digital signature module."""

import os

from app.core.signature import generate_key_pair, sign_data, verify_signature


def test_sign_without_key():
    """Without a key configured, should return hash-only signature."""
    data = b"test document data"
    sig = sign_data(data)
    assert sig is not None
    assert sig.startswith("hash-only:")


def test_verify_hash_only_signature():
    data = b"test document data"
    sig = sign_data(data)
    assert verify_signature(data, sig) is True
    assert verify_signature(b"tampered data", sig) is False


def test_generate_key_pair():
    private_pem, public_pem = generate_key_pair()
    assert b"BEGIN PRIVATE KEY" in private_pem
    assert b"BEGIN PUBLIC KEY" in public_pem


def test_sign_and_verify_with_key(tmp_path):
    private_pem, _ = generate_key_pair()
    key_path = tmp_path / "test_key.pem"
    key_path.write_bytes(private_pem)

    os.environ["SIGNING_PRIVATE_KEY_PATH"] = str(key_path)

    from importlib import reload
    from app.core import config
    reload(config)
    from app.core import signature
    reload(signature)

    data = b"document to sign"
    sig = signature.sign_data(data)
    assert not sig.startswith("hash-only:")
    assert signature.verify_signature(data, sig) is True
    assert signature.verify_signature(b"tampered", sig) is False

    del os.environ["SIGNING_PRIVATE_KEY_PATH"]
    reload(config)
    reload(signature)
