from typing import List, Optional

from pydantic import BaseModel


class PermissionCreate(BaseModel):
    name: str
    description: Optional[str] = None


class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    permissions: Optional[List[int]] = []


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    roles: Optional[List[int]] = []
