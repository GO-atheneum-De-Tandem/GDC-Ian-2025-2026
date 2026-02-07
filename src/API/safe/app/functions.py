# authentication imports
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, Argon2Error
import jwt

# algemene imports
from datetime import datetime, timedelta

# config imports
from app.config import settings
from sqlalchemy import select
from app.models import User
from app.database import AsyncSessionLocal

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

async def verify_jwt_token(token: str):
    """Verify a JWT token and return (is_valid: bool, payload: dict|None)."""
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return True, payload
    except jwt.ExpiredSignatureError:
        return False, None
    except jwt.InvalidTokenError:
        return False, None
    except Exception as e:
        raise RuntimeError("Token verification failed") from e

async def has_level_access_by_jwt(payload: dict, level: int) -> bool:
    """Check whether the given JWT payload grants user access."""

    if not isinstance(payload, dict) or level is None:
        return False
    role = payload.get("role")
    if role is None:
        return False

    try:
        role_int = int(role)
    except (TypeError, ValueError):
        return False

    return role_int <= level


async def has_level_access_by_db(payload: dict, level: int) -> bool:
    """Check whether the user identified in `payload` has access by querying the DB."""

    if not isinstance(payload, dict) or level is None:
        return False

    sub = payload.get("sub")
    if sub is None:
        return False
    try:
        user_id = int(sub)
    except (TypeError, ValueError):
        return False

    query = select(User).where(User.id == user_id)
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(query)
            user = result.scalars().first()
    except Exception:
        return False

    if not user:
        return False

    try:
        role_int = int(user.role)
    except (TypeError, ValueError):
        return False

    return role_int <= level