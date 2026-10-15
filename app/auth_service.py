import hashlib
import os
from typing import Optional
from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserRegister


def hash_password(password: str) -> str:
    """Hashes a password with salt using PBKDF2 HMAC SHA-256."""
    salt = os.urandom(16).hex()
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        bytes.fromhex(salt),
        100000
    )
    return f"{salt}${key.hex()}"


def verify_password(stored_password_hash: str, provided_password: str) -> bool:
    """Verifies a password against the stored PBKDF2 hash."""
    try:
        salt, key_hex = stored_password_hash.split('$')
        computed_key = hashlib.pbkdf2_hmac(
            'sha256',
            provided_password.encode('utf-8'),
            bytes.fromhex(salt),
            100000
        )
        return computed_key.hex() == key_hex
    except Exception:
        return False


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Retrieves a user by lowercase username."""
    return db.query(User).filter(User.username == username.strip().lower()).first()


def create_user(db: Session, user_in: UserRegister) -> User:
    """Creates a new user with hashed password stored in the database."""
    hashed = hash_password(user_in.password)
    db_user = User(
        username=user_in.username.strip().lower(),
        password_hash=hashed
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
