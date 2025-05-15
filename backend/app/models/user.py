from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql import func
from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(db.DateTime, server_default=func.now())
    updated_at = Column(db.DateTime, onupdate=func.now())

    def __repr__(self):
        return f"<User {self.username}>"
