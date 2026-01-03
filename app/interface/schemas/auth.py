from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    firstname: str
    lastname: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    firstname: str
    lastname: str
    is_active: bool
    is_superuser: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime

class LoginResponse(BaseModel):
    message: str = "Login successful"
    user: UserResponse

class TokenData(BaseModel):
    user_id: Optional[str] = None

class RefreshToken(BaseModel):
    refresh_token: str