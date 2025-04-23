from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.models.user import UserCreate, Token, UserInDB
from app.services.auth_service import auth_service
from app.models.user import UserBase

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserBase, status_code=201)
async def register(user: UserCreate):
    return auth_service.create_user(user)

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = auth_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserBase)
async def read_users_me(current_user: UserInDB = Depends(auth_service.get_current_user)):
    return current_user