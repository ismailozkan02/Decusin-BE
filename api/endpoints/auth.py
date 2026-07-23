from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.config import settings
from core.dependencies import get_current_user
from core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from db.session import get_db
from schemas.auth import (
    ApiResponse,
    LoginRequest,
    RegisterRequest,
    RefreshItem,
    RefreshTokenRequest,
    SessionPayload,
    TokenItem,
    UserInfo,
)
from services.auth_service import (
    authenticate_user,
    get_user_by_email,
    get_user_by_id,
    register_user,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


def build_session_payload(user_id: str, access_token: str, refresh_token: str) -> SessionPayload:
    access_expires = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    refresh_expires = datetime.now(timezone.utc) + timedelta(days=7)
    return SessionPayload(
        id=user_id,
        access=TokenItem(
            token=access_token,
            expire=int(access_expires.timestamp()),
        ),
        refresh=RefreshItem(
            token=refresh_token,
            expire=int(refresh_expires.timestamp()),
        ),
    )


@router.post("/register", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
):
    if get_user_by_email(db, payload.email):
        return ApiResponse(
            success=False,
            payload=None,
            error={"message": "Email already registered", "code": "EMAIL_TAKEN", "args": []},
        )

    user = register_user(
        db, payload.email, payload.password, payload.first_name, payload.last_name
    )
    return ApiResponse(success=True, payload={"user": UserInfo.model_validate(user).model_dump()}, error=None)


@router.post("/login", response_model=ApiResponse)
async def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        return ApiResponse(
            success=False,
            payload=None,
            error={"message": "Incorrect email or password", "code": "AUTH_FAILED", "args": []},
        )

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    session_payload = build_session_payload(str(user.id), access_token, refresh_token)

    return ApiResponse(
        success=True,
        payload={"session": session_payload.model_dump(), "user": UserInfo.model_validate(user).model_dump()},
        error=None,
    )


@router.post("/refresh", response_model=ApiResponse)
async def refresh(
    payload: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    decoded = decode_refresh_token(payload.refresh_token)
    if not decoded or "sub" not in decoded:
        return ApiResponse(
            success=False,
            payload=None,
            error={"message": "Invalid refresh token", "code": "INVALID_REFRESH_TOKEN", "args": []},
        )

    user = get_user_by_id(db, decoded["sub"])
    if not user:
        return ApiResponse(
            success=False,
            payload=None,
            error={"message": "User not found", "code": "USER_NOT_FOUND", "args": []},
        )

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    session_payload = build_session_payload(str(user.id), access_token, refresh_token)

    return ApiResponse(
        success=True,
        payload={"session": session_payload.model_dump(), "user": UserInfo.model_validate(user).model_dump()},
        error=None,
    )


@router.post("/logout", response_model=ApiResponse)
async def logout(current_user: dict = Depends(get_current_user)):
    return ApiResponse(success=True, payload=None, error=None)


@router.get("/me", response_model=ApiResponse)
async def me(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = get_user_by_id(db, current_user["sub"])
    if not user:
        return ApiResponse(
            success=False,
            payload=None,
            error={"message": "User not found", "code": "USER_NOT_FOUND", "args": []},
        )
    return ApiResponse(success=True, payload={"user": UserInfo.model_validate(user).model_dump()}, error=None)
