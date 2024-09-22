# from auth.utils import get_current_user
# from core.models import User
# from database.core import get_async_db
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession

# from .schemas import OrganisationCreate, OrganisationUpdate
# from .services import create_organisation, get_all_organisations, update_organisation

# organisation_router = APIRouter(prefix="/organisations", tags=["Organisations"])


# @organisation_router.get("")
# async def list_organisations(db_session: AsyncSession = Depends(get_async_db)):
#     orgs = await get_all_organisations(db_session=db_session)

#     return {"organisations": [org.to_dict() for org in orgs]}


# @organisation_router.post("", status_code=status.HTTP_201_CREATED)
# async def create_new_organisation(
#     org_data: OrganisationCreate,
#     db_session: AsyncSession = Depends(get_async_db),
#     current_user: User = Depends(get_current_user),
# ):
#     new_org = await create_organisation(db_session, org_data, current_user)
#     return {"organisation": new_org.to_dict()}


# @organisation_router.put("/{org_id}")
# async def update_existing_organisation(
#     org_id: int,
#     org_data: OrganisationUpdate,
#     db_session: AsyncSession = Depends(get_async_db),
#     current_user: User = Depends(get_current_user),
# ):
#     updated_org = await update_organisation(db_session, org_id, org_data, current_user)
#     if not updated_org:
#         raise HTTPException(status_code=404, detail="Organisation not found")
#     return {"organisation": updated_org.to_dict()}
