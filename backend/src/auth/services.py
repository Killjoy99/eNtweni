from datetime import datetime, timedelta

from core.config import settings
from core.models import User
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import TokenResponse, UserCreate
from .utils import (
    decode_token,
    generate_access_token,
    generate_password_hash,
    generate_refresh_token,
    verify_password_hash,
)


async def create_user_account(user_in: UserCreate, db_session: AsyncSession):
    query = select(User).where(User.email == user_in.email)
    result = await db_session.execute(query)
    user = result.scalar_one_or_none()

    if user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Email already registered",
        )

    hashed_password = await generate_password_hash(user_in.password)
    new_user = User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        email=user_in.email.lower(),
        password=hashed_password,
        is_active=True,  # or False if you want to verify first
        is_verified=False,  # or False if you want to verify first
        updated_at=datetime.now(),
    )

    db_session.add(new_user)
    await db_session.commit()
    await db_session.refresh(new_user)

    return new_user


async def create_token(user_in: OAuth2PasswordRequestForm, db_session: AsyncSession):
    query = select(User).where(User.email == user_in.username)
    result = await db_session.execute(query)
    user = result.scalar_one_or_none()

    if not user or not await verify_password_hash(user_in.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    await _verify_user_access(user=user)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await generate_access_token(
        data={"id": user.id}, expires=access_token_expires
    )
    refresh_token = await generate_refresh_token(data={"id": user.id})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_token_expires.seconds,
    )


async def create_refresh_token(token: str, db_session: AsyncSession):
    payload = await decode_token(token=token)
    user_id = payload.get("id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    query = await db_session.execute(select(User).where(User.id == user_id))
    user = query.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return await _get_user_token(user=user, refresh_token=token)


async def _verify_user_access(user: User):
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your account is inactive. Please contact support",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your account is not verified. We have sent the verification email",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def _get_user_token(user: User, refresh_token=None):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await generate_access_token(
        data={"id": user.id}, expires=access_token_expires
    )

    if not refresh_token:
        refresh_token = await generate_refresh_token(data={"id": user.id})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_token_expires.seconds,
    )
