from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from src.security.jwt import decode_access_token
from src.security.schema import Credentials
from fastapi import Depends, HTTPException, status
from src.security.jwt import decode_access_token, InvalidTokenError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def authenticate(
    token: str = Depends(oauth2_scheme),
):
    try:
        user_id = decode_access_token(token)
        return Credentials(user_id=user_id)

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )