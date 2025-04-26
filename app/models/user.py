from pydantic import BaseModel, EmailStr
from typing import Optional, List, Union, Dict
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    id: UUID
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime
    last_login: Optional[datetime] = None
    listening_history: List[Dict[str, Union[int, datetime]]] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
