from datetime import timedelta
from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.utils.jwt import (verify_password, get_password_hash,
                           create_access_token)
from config import settings


class AuthService:

    def __init__(self, db: Session):
        self.db = db

    def authenticate_user(self, username: str,
                          password: str) -> Optional[User]:
        user = self.db.query(User).filter(User.username == username).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def create_access_token_for_user(self, user: User) -> str:
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(data={"sub": user.username},
                                   expires_delta=access_token_expires)

    def create_user(self, username: str, password: str, email: str) -> User:
        hashed_password = get_password_hash(password)
        user = User(username=username,
                    email=email,
                    hashed_password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
