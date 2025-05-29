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


from pydantic import BaseModel, Field


class LoginForm(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "testuser",
                "password": "testpassword"
            }
        }


import logging

logger = logging.getLogger(__name__)


@router.post("/login", response_model=Token)
async def simple_login(form_data: LoginForm, db: Session = Depends(get_db)):
    try:
        auth_service = AuthService(db)
        user = auth_service.authenticate_user(form_data.username,
                                              form_data.password)
        if not user:
            logger.warning(f"Login failed for username: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": "Authentication failed",
                    "message": "Invalid username or password"
                },
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = auth_service.create_access_token_for_user(user)
        logger.info(f"User {form_data.username} logged in successfully")
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={
                                "error": "Internal server error",
                                "message": str(e)
                            })


class RegisterForm(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(
        ..., pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    password: str = Field(..., min_length=8, max_length=100)
    confirm_password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "newuser",
                "email": "user@example.com",
                "password": "strongpassword",
                "confirm_password": "strongpassword"
            }
        }


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(form_data: RegisterForm,
                        db: Session = Depends(get_db)):
    if form_data.password != form_data.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Passwords do not match")

    auth_service = AuthService(db)
    try:
        user = auth_service.create_user(username=form_data.username,
                                        password=form_data.password,
                                        email=form_data.email)
        return {
            "message": "User created successfully",
            "user_id": user.id,
            "email": user.email
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e))
    except Exception as e:
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error")
