from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserCreate(BaseModel):
    username: str
    password: str
    email: str


class UserInDB(UserCreate):
    hashed_password: str
