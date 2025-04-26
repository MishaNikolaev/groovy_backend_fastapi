from datetime import datetime, timedelta
from typing import Optional
import uuid
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..models.user import UserInDB, TokenData, UserCreate, UserUpdate
import os
from typing import Dict

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


class AuthService:

    def __init__(self):
        self.users_db: Dict[str, UserInDB] = {}
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)


    def get_user(self, username: str) -> Optional[UserInDB]:
        for user in self.users_db.values():
            if user.username == username:
                return user
        return None

    def get_user_by_id(self, user_id: str) -> Optional[UserInDB]:
        return self.users_db.get(user_id)

    def authenticate_user(self, username: str, password: str):
        user = self.get_user(username)
        if not user or not self.verify_password(password, user.hashed_password):
            return None
        return user

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def create_user(self, user: UserCreate) -> UserInDB:
        if self.get_user(user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

        hashed_password = self.get_password_hash(user.password)
        user_id = str(uuid.uuid4())
        db_user = UserInDB(
            id=user_id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password,
            created_at=datetime.utcnow()
        )
        self.users_db[user_id] = db_user
        return db_user

    def update_user(self, user_id: str, user_update: UserUpdate) -> UserInDB:
        user = self.users_db.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        update_data = user_update.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = self.get_password_hash(update_data.pop("password"))

        updated_user = user.model_copy(update=update_data)
        self.users_db[user_id] = updated_user
        return updated_user

    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception

        user = self.get_user(token_data.username)
        if user is None:
            raise credentials_exception
        return user

    async def get_current_active_user(self, current_user: UserInDB = Depends(get_current_user)):
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

    async def get_current_admin_user(self, current_user: UserInDB = Depends(get_current_user)):
        if not current_user.is_superuser:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return current_user


auth_service = AuthService()