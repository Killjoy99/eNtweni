from datetime import datetime, timedelta
from typing import Optional

import jwt
from core.config import settings
from core.models import User
from database.core import get_async_db
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def generate_password_hash(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


async def verify_password_hash(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def generate_access_token(data: dict, expires: timedelta):
    payload = data.copy()
    expires_in = datetime.utcnow() + expires
    payload.update({"exp": expires_in})

    return jwt.encode(
        payload=payload,
        key=settings.JWT_ACCESS_SECRET_KEY,
        algorithm=settings.ENCRYPTION_ALGORITHM,
    )


async def generate_refresh_token(data: dict):
    return jwt.encode(
        payload=data,
        key=settings.JWT_ACCESS_SECRET_KEY,
        algorithm=settings.ENCRYPTION_ALGORITHM,
    )


async def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_ACCESS_SECRET_KEY,
            algorithms=[settings.ENCRYPTION_ALGORITHM],
        )
    except PyJWTError:
        return None

    return payload


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db_session: AsyncSession = Depends(get_async_db),
) -> Optional[User]:
    payload = await decode_token(token=token)
    if not payload or not isinstance(payload, dict):
        return None

    user_id = payload.get("id")
    if not user_id:
        return None

    query = await db_session.execute(select(User).where(User.id == user_id))
    user = query.scalar_one_or_none()

    return user


class JWTAuth(BaseHTTPMiddleware):
    async def authenticate(self, request: Request):
        # If the user is not logged in
        guest = AuthCredentials(["unauthenticated"]), UnauthenticatedUser()

        # Check if authorization header is present
        if "authorization" not in request.headers:
            return guest

        # Extract token from the headers
        auth_header = request.headers.get("authorization")
        if not auth_header:
            return guest

        # Split "Bearer <token>" to extract the actual token
        token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else None
        if not token:
            return guest

        # Retrieve the current user from the token using get_current_user
        db_session: AsyncSession = await get_async_db().__anext__()
        user = await get_current_user(token=token, db_session=db_session)

        if not user:
            return guest

        return AuthCredentials(["authenticated"]), user

    async def dispatch(self, request: Request, call_next):
        credentials, user = await self.authenticate(request)
        request.scope["auth"] = credentials
        request.scope["user"] = user
        response = await call_next(request)
        return response
