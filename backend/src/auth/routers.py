from core.models import User
from database.core import get_async_db
from fastapi import APIRouter, Depends, Header, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserCreate, UserResponse
from .services import create_refresh_token, create_token, create_user_account
from .utils import get_current_user

# Create the router
auth_router = APIRouter(prefix="/auth", tags=["Auth"])
authenticated_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    dependencies=[Depends(get_current_user)],
)


auth_router = APIRouter(prefix="/auth", tags=["Auth"])
authenticated_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
async def register_user(
    user: UserCreate, db_session: AsyncSession = Depends(get_async_db)
):
    new_user = await create_user_account(user_in=user, db_session=db_session)
    return new_user


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def authenticate_user(
    user: OAuth2PasswordRequestForm = Depends(),
    db_session: AsyncSession = Depends(get_async_db),
):
    return await create_token(user_in=user, db_session=db_session)


@auth_router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_access_token(
    refresh_token: str = Header(), db_session: AsyncSession = Depends(get_async_db)
):
    return await create_refresh_token(token=refresh_token, db_session=db_session)


@auth_router.get(
    "/me", response_model=UserResponse, dependencies=[Depends(get_current_user)]
)
async def get_loged_in_user(current_user: User = Depends(get_current_user)):
    return current_user
