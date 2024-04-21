import binascii
import hashlib
import os
import secrets
import string

_PBKDF2_HASH_NAME = "SHA256"
_PBKDF2_ITERATIONS = 100_000


def generate_hashed_password(password: str) -> str:
    pbkdf2_salt = os.urandom(16)
    pw_hash = hashlib.pbkdf2_hmac(
        _PBKDF2_HASH_NAME,
        password.encode(),
        pbkdf2_salt,
        _PBKDF2_ITERATIONS,
    )

    return "%s:%s" % (
        binascii.hexlify(pbkdf2_salt).decode(),
        binascii.hexlify(pw_hash).decode(),
    )


def validate_hashed_password(password: str, hashed_password: str) -> bool:
    pbkdf2_salt_hex, pw_hash_hex = hashed_password.split(":")

    pw_challenge = hashlib.pbkdf2_hmac(
        _PBKDF2_HASH_NAME,
        password.encode(),
        binascii.unhexlify(pbkdf2_salt_hex),
        _PBKDF2_ITERATIONS,
    )

    return pw_challenge == binascii.unhexlify(pw_hash_hex)


def make_random_string(
    length: int,
    letters: str = string.ascii_letters + string.digits,
) -> str:
    return "".join((secrets.choice(letters) for _ in range(length)))
