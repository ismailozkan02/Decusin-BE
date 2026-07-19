import uuid

from sqlalchemy.orm import Session

from core.security import hash_password, verify_password
from models.sys_account import SysAccount


def get_user_by_email(db: Session, email: str) -> SysAccount | None:
    return db.query(SysAccount).filter(SysAccount.email == email).first()


def authenticate_user(db: Session, email: str, password: str) -> SysAccount | None:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        return None
    return user


def register_user(
    db: Session,
    email: str,
    password: str,
    first_name: str | None,
    last_name: str | None,
) -> SysAccount:
    user = SysAccount(
        email=email,
        password=hash_password(password),
        first_name=first_name,
        last_name=last_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: str) -> SysAccount | None:
    try:
        account_id = uuid.UUID(str(user_id))
    except ValueError:
        return None

    return db.query(SysAccount).filter(SysAccount.id == account_id).first()
