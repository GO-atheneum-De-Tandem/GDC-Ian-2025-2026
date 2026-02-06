# authentication imports
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, Argon2Error
import jwt

# algemene imports
from datetime import datetime, timedelta

# config imports
from app.config import settings

async def create_password_hash(password: str) -> str:
    """Create a hashed password using Argon2id. Expects a plain password string. Returns the hashed password string."""
    
    ph = PasswordHasher(
        time_cost=settings.HASH_TIME_COST,
        memory_cost=settings.HASH_MEMORY_COST,
        parallelism=settings.HASH_PARALLELISM,
        salt_len=settings.HASH_SALT_LENGTH,
        hash_len=settings.HASH_HASH_LENGTH,
    )
    try:
        return ph.hash(password)
    except Argon2Error as e:
        raise RuntimeError("Password hashing failed") from e

async def verify_password(stored_hash: str, password: str) -> bool:
    """Verify a plain password against a stored Argon2 hash. Expects stored_hash and password. Returns boolean."""

    ph = PasswordHasher()
    try:
        ph.verify(stored_hash, password)
        return True
    except VerifyMismatchError:
        return False
    except Argon2Error as e:
        raise RuntimeError("Password verification failed") from e
    
async def create_jwt_token(user_id: int, username: str, role: int):
    """Create a JWT token and return (token, expiration_datetime). Expects user_id, username, role."""

    now = datetime.utcnow()
    exp = now + timedelta(minutes=settings.JWT_EXP_MINUTES)
    payload = {
        "sub": str(user_id),
        "username": username,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }

    try:
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    except Exception as e:
        raise RuntimeError("Token generation failed") from e

    return token, exp