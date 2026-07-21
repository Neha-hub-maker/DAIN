import hashlib
import secrets
import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "dain_dunite_jwt_secret_key_environment_override"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

def hash_password(password: str) -> str:
    """
    Hash password using PBKDF2-HMAC-SHA256 with 100,000 iterations and random salt.
    Zero external dependencies. Format: <salt>$<hex_hash>
    """
    salt = secrets.token_hex(16)
    pw_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return f"{salt}${pw_hash}"

def verify_password(plain_password: str, hashed_password: str | None) -> bool:
    """
    Verify password against stored salt$hash using timing-attack safe comparison.
    """
    if not hashed_password or '$' not in hashed_password:
        return False
    try:
        salt, stored_hash = hashed_password.split('$', 1)
        computed_hash = hashlib.pbkdf2_hmac(
            'sha256',
            plain_password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        return secrets.compare_digest(computed_hash, stored_hash)
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Generate a signed JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    """
    Decode and validate JWT access token signature and expiration.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
