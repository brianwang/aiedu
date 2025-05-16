from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import Token
from app.services.auth_service import AuthService
from app.utils.jwt import get_current_user
from config import settings
from database import get_db

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(form_data.username,
                                          form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_access_token_for_user(user)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
async def register_user(username: str,
                        password: str,
                        email: str,
                        db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    try:
        user = auth_service.create_user(username, password, email)
        return {"message": "User created successfully", "user_id": user.id}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e))
