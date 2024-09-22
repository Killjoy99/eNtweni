import logging

# from auth.services import get_current_user
from database.core import get_async_db
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils import templates

# from .utils import require_permission

logger = logging.getLogger(__name__)

home_router = APIRouter(tags=["Home"])


@home_router.get("/", name="index", tags=["Home"])
def index(request: Request):
    return templates.TemplateResponse(request=request, name="core/index.html")


@home_router.get("/healthcheck", name="healthcheck", tags=["Home"])
async def healthcheck(
    db_session: AsyncSession = Depends(get_async_db),
):
    return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "STATUS_OK"})


# @home_router.get("/home", name="home", dependencies=[Depends(get_current_user)])
# async def home(
#     request: Request,
#     response: Response,
#     db_session: AsyncSession = Depends(get_async_db),
#     is_template: Optional[bool] = Depends(check_accept_header),
# ):
#     """Render the home page or return JSON response based on the request header."""
#     if is_template:
#         # Get cookies
#         access_token = request.cookies.get("access_token")
#         refresh_token = request.cookies.get("refresh_token")

#         user_info = {}
#         error_message = None

#         try:
#             # Decode the access token to get user information
#             if access_token:
#                 user_info = decode_access_token(access_token)
#             elif refresh_token:
#                 # Optionally, decode the refresh token if access token is not present
#                 user_info = decode_refresh_token(refresh_token)
#             else:
#                 error_message = "No tokens found in cookies"

#         except Exception as e:
#             error_message = f"Error decoding tokens: {e}"
#             logger.error(error_message)

#         # Render the template with user information or error message
#         return templates.TemplateResponse(
#             request=request,
#             name="home.html",
#             context={"user_info": user_info, "data": {}},
#         )

#     else:
#         # Return a JSON response for non-template requests
#         return JSONResponse(content={"message": "Home endpoint accessed"})


@home_router.get("/microservices", name="microservices_home")
async def microservices_home():
    return {"detail": "List of all Available microservices"}


# Create roles and permissions
# @home_router.post("/roles/")
# async def role_create(
#     role: RoleCreate, db_session: AsyncSession = Depends(get_async_db)
# ):
#     return await create_role(role=role, db_session=db_session)


# @home_router.post("/permissions/")
# async def permission_create(
#     permission: PermissionCreate, db_session: AsyncSession = Depends(get_async_db)
# ):
#     return await create_permission(permission=permission, db_session=db_session)


# Test permission routes and access
# @home_router.get(
#     "/admin-dashboard", dependencies=[Depends(require_permission("admin"))]
# )
# async def test_permissions():
#     return {"detail": "Welcome to the admin dashboard player"}
