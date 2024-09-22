# import logging

# from auth.utils import generate_password_hash
# from core.models import Permission, Role, User
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession

# from .schemas import UserRegistrationSchema

# logger = logging.getLogger(__name__)


# DEFAULT_CHUNK_SIZE = 1024 * 1024 * 1  # 1 megabyte (1Mb)


# async def create_user(
#     db_session: AsyncSession, *, user_schema: UserRegistrationSchema
# ) -> User:
#     # Hash the password
#     hashed_password = await generate_password_hash(user_schema.password)

#     # Retrieve or create the default role
#     default_role_name = "user"  # adjust to meet your standards
#     default_role = await db_session.execute(
#         select(Role).where(Role.name == default_role_name)
#     )
#     default_role = default_role.scalar_one_or_none()

#     # Create the role if its not found
#     if not default_role:
#         default_permissions = ["read"]  # adjust to meet your standards
#         permissions = []

#         for perm_name in default_permissions:
#             perm = await db_session.execute(
#                 select(Permission).where(Permission.name == perm_name)
#             )
#             perm = perm.scalar_one_or_none()
#             if not perm:
#                 perm = Permission(name=perm_name)
#                 db_session.add(perm)
#             permissions.append(perm)

#         default_role = Role(name=default_role_name, permissions=permissions)
#         db_session.add(default_role)

#         await db_session.commit()

#     new_user = User(
#         username=user_schema.username.lower(),
#         email=user_schema.email.lower(),
#         first_name=user_schema.first_name,
#         last_name=user_schema.last_name,
#         password=hashed_password,
#         roles=[default_role],  # Assign the default role
#     )

#     db_session.add(new_user)
#     await db_session.commit()
#     await db_session.refresh(new_user)

#     return new_user


# class ImageSaver:
#     @classmethod
#     def save_user_image(cls, user, uploaded_image):
#         pass
