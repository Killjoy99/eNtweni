import logging
from os import path

import redis.asyncio as aioredis
from admin.admin import UserAdmin
from auth.routers import auth_router
from auth.utils import JWTAuth
from core.config import settings
from core.routers import home_router
from core.utils import templates
from database.core import async_engine, init_models
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi_limiter import FastAPILimiter
from fastapi_offline import FastAPIOffline

# from organisation.routers import organisation_router
from plugins.manager import PluginManager
from pyinstrument import Profiler
from pyinstrument.renderers.html import HTMLRenderer  # noqa: F401

# from registration.routers import account_router
from sqladmin import Admin


class PyInstrumentMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            profiler = Profiler()
            profiler.start()
            await self.app(scope, receive, send)
            profiler.stop()
            profiler.open_in_browser()
        else:
            await self.app(scope, receive, send)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        # Add more handlers if needed, e.g., FileHandler
    ],
)
logger = logging.getLogger(__name__)


app = FastAPIOffline(
    title="eNtweniBooking",
    description="Welcome to eNtweniBooking's API documentation!",
    version="0.1.2",
)


plugin_manager = PluginManager(app=app)

# app.add_middleware(PyInstrumentMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust according to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(JWTAuth)


@app.middleware("http")
async def default_page(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        # Render the 404 page using the custom template
        template_response = templates.TemplateResponse(
            "404.html", {"request": request, "data": {}, "error_message": "Not Found"}
        )
        return HTMLResponse(content=template_response.body.decode(), status_code=404)
    return response


# Rate limiting
@app.on_event("startup")
async def startup():
    # Load the startup logic
    redis_limiter = aioredis.from_url(url="redis://localhost:6379")
    await FastAPILimiter().init(redis=redis_limiter)

    # Initialise the database models (Schema)
    await init_models()

    # Register core (default) microservices
    # plugin_manager.initialise_microservices()


# Routes management
app.include_router(home_router)
app.include_router(auth_router)
# app.include_router(organisation_router)
# Register microservices
plugin_manager.register_microservice(microservice_name="booking")
plugin_manager.register_microservice(microservice_name="school_management")
# plugin_manager.register_microservice(microservice_name="budgeting")
# plugin_manager.register_microservice(microservice_name="housing")

# Initialise the microservices
plugin_manager.initialise_microservices()

# Test disable a microservice
# plugin_manager.disable_microservice(microservice_name="school_management")
# plugin_manager.disable_microservice(microservice_name="booking")


admin = Admin(app, async_engine)
admin.add_view(UserAdmin)
# admin.add_view(OrganisationAdmin)
# admin.add_view(OrganisationUserAdmin)
# admin.add_view(RoleAdmin)
# admin.add_view(PermissionAdmin)


if settings.STATIC_DIR and path.isdir(settings.STATIC_DIR):
    # Consider changing the route for static files to avoid conflicts
    app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
