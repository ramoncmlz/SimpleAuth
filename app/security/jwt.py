import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.services.user_service import find_user_by_username

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bearer_scheme = HTTPBearer()


def create_access_token(subject: str, session_version: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "sv": session_version, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


def get_current_username(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> str:
    payload = decode_access_token(credentials.credentials)
    if not payload or "sub" not in payload or "sv" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )

    username = payload["sub"]
    token_session_version = payload["sv"]

    user = find_user_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found for this token.",
        )

    if int(user["session_active"]) != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session is not active.",
        )

    if int(user["session_version"]) != int(token_session_version):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session is no longer active. Please log in again.",
        )

    return username
