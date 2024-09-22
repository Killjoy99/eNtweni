# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
# from .models import Organisation
# from .schemas import OrganisationCreate, OrganisationUpdate
# from core.models import User

# async def create_organisation(db_session: AsyncSession, org_data: OrganisationCreate, creator: User) -> Organisation:
#     new_org = Organisation(**org_data.model_dump(), creator_id=creator.id)
#     db_session.add(new_org)
#     await db_session.commit()
#     await db_session.refresh(new_org)
#     return new_org

# async def update_organisation(db_session: AsyncSession, org_id: int, org_data: OrganisationUpdate, current_user: User) -> Organisation | None:
#     query = select(Organisation).where(Organisation.id == org_id, Organisation.is_deleted.is_(False))
#     result = await db_session.execute(query)
#     org = result.scalar_one_or_none()

#     if org and (org.creator_id == current_user.id or current_user.is_superuser):
#         for key, value in org_data.model_dump(exclude_unset=True).items():
#             setattr(org, key, value)
#         await db_session.commit()
#         await db_session.refresh(org)
#         return org
#     return None

# async def get_all_organisations(db_session: AsyncSession):
#     query = select(Organisation).where(Organisation.is_deleted.is_(False))
#     result = await db_session.execute(query)
#     orgs = result.scalars().all()

#     return orgs
