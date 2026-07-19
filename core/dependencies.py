from fastapi import Depends, HTTPException, Request, status

from core.security import decode_access_token


async def get_current_user(request: Request) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    authorization = request.headers.get("authorization")
    if not authorization:
        raise credentials_exception

    token = authorization
    if authorization.lower().startswith("bearer "):
        token = authorization[7:]

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    sub: str | None = payload.get("sub")
    if sub is None:
        raise credentials_exception
    return payload
