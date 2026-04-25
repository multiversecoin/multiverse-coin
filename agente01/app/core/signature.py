"""Digital signature for report integrity — RSA with SHA-256."""

import base64
from typing import Optional

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa, utils
from cryptography.exceptions import InvalidSignature

from app.core.config import settings
from app.core.hashing import compute_sha256_from_bytes


def _load_private_key():
    pem_data = None

    if settings.SIGNING_PRIVATE_KEY_PEM:
        pem_data = settings.SIGNING_PRIVATE_KEY_PEM.encode()
    elif settings.SIGNING_PRIVATE_KEY_PATH:
        with open(settings.SIGNING_PRIVATE_KEY_PATH, "rb") as f:
            pem_data = f.read()

    if pem_data is None:
        return None

    return serialization.load_pem_private_key(pem_data, password=None)


def _get_public_key_from_private(private_key):
    return private_key.public_key()


def generate_key_pair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def sign_data(data: bytes) -> Optional[str]:
    private_key = _load_private_key()
    if private_key is None:
        file_hash = compute_sha256_from_bytes(data)
        return f"hash-only:{file_hash}"

    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return base64.b64encode(signature).decode("utf-8")


def verify_signature(data: bytes, signature_b64: str) -> bool:
    if signature_b64.startswith("hash-only:"):
        expected_hash = signature_b64.split(":", 1)[1]
        return compute_sha256_from_bytes(data) == expected_hash

    private_key = _load_private_key()
    if private_key is None:
        return False

    public_key = _get_public_key_from_private(private_key)
    signature = base64.b64decode(signature_b64)

    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except InvalidSignature:
        return False
