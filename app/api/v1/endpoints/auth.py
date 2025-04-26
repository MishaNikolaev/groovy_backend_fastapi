from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.models.user import UserCreate, Token, UserInDB, UserBase, UserUpdate
from app.services.auth_service import auth_service
from typing import Annotated

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserBase, status_code=201)
async def register(user: UserCreate):
    return auth_service.create_user(user)

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
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
async def read_users_me(
    current_user: Annotated[UserInDB, Depends(auth_service.get_current_active_user)]
):
    return current_user

@router.put("/me", response_model=UserBase)
async def update_user_me(
    user_update: UserUpdate,
    current_user: Annotated[UserInDB, Depends(auth_service.get_current_active_user)]
):
    return auth_service.update_user(str(current_user.id), user_update)

@router.post("/refresh", response_model=Token)
async def refresh_token(
    current_user: Annotated[UserInDB, Depends(auth_service.get_current_active_user)]
):
    access_token_expires = timedelta(minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}