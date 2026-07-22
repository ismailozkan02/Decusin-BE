import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Enum, String, Uuid

from db.base import Base


class RoleEnum(str, enum.Enum):
    guest = "guest"
    student = "student"
    parent = "parent"
    teacher = "teacher"
    admin = "admin"


class SysAccount(Base):
    __tablename__ = "sys_account"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    deleted_at = Column(DateTime, nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.guest)
    is_active = Column(Boolean, default=True)
