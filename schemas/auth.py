import uuid
from typing import Any

from pydantic import BaseModel, EmailStr

from models.sys_account import RoleEnum


class ApiResponse(BaseModel):
    success: bool
    payload: Any | None = None
    error: Any | None = None


class TokenItem(BaseModel):
    token: str
    expire: int | None = None


class RefreshItem(BaseModel):
    token: str
    expire: int | None = None


class SessionPayload(BaseModel):
    id: str
    access: TokenItem
    refresh: RefreshItem


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserInfo(BaseModel):
    id: uuid.UUID
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    role: RoleEnum = RoleEnum.guest
    is_active: bool = True
    language: str | None = None
    base_url: str | None = None

    model_config = {"from_attributes": True}


class AuthPayload(BaseModel):
    session: SessionPayload
    user: UserInfo | None = None
