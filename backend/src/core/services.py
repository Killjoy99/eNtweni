# from database.core import get_async_db
# from fastapi import Depends
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession

# from .models import Permission, Role
# from .schemas import PermissionCreate, RoleCreate


# async def create_role(
#     role: RoleCreate, db_session: AsyncSession = Depends(get_async_db)
# ):
#     new_role = Role(name=role.name, description=role.description)
#     if role.permissions:
#         permissions = await db_session.execute(
#             select(Permission).where(Permission.id.in_(role.permissions))
#         )
#         new_role.permissions.extend(permissions.scalars().all())

#     db_session.add(new_role)
#     await db_session.commit()
#     await db_session.refresh(new_role)

#     return new_role


# async def create_permission(
#     permission: PermissionCreate, db_session: AsyncSession = Depends(get_async_db)
# ):
#     new_permission = Permission(
#         name=permission.name, description=permission.description
#     )
#     db_session.add(new_permission)
#     await db_session.commit()
#     await db_session.refresh(new_permission)

#     return new_permission
