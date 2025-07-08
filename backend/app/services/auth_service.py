from datetime import timedelta
from typing import Optional

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt as PyJWT

from app.models.user import User
from app.utils.jwt import (verify_password, get_password_hash,
                           create_access_token)
from config import settings
from database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

class AuthService:

    def __init__(self, db: Session):
        self.db = db

    def authenticate_user(self, username: str,
                          password: str) -> Optional[User]:
        user = self.db.query(User).filter(User.username == username).first()
        if not user:
            return None
        
        # 支持两种密码验证方式
        # 1. 检查哈希密码
        if user.hashed_password and str(user.hashed_password) and verify_password(password, str(user.hashed_password)):
            return user
        
        # 2. 检查明文密码
        if user.password and str(user.password) == password:
            return user
            
        return None

    def create_access_token_for_user(self, user: User) -> str:
        access_token_expires = timedelta(
            minutes=settings.access_token_expire_minutes)
        return create_access_token(data={"sub": user.username},
                                   expires_delta=access_token_expires)

    def create_user(self, username: str, password: str, email: str) -> User:
        hashed_password = get_password_hash(password)
        user = User(username=username,
                    email=email,
                    password=password,  # 同时保存明文密码
                    hashed_password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """FastAPI依赖，获取当前登录用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = PyJWT.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
