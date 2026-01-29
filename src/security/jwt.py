from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import uuid

from src.core.settings import settings


class InvalidTokenError(Exception):
    pass


def create_access_token(user_id: uuid.UUID) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub": str(user_id),
        "exp": expire,
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

def decode_access_token(token: str) -> uuid.UUID:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        sub = payload.get("sub")
        if sub is None:
            raise InvalidTokenError("Missing subject")

        return uuid.UUID(sub)

    except (JWTError, ValueError):
        raise InvalidTokenError("Invalid or expired token")




