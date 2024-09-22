import logging
from importlib import import_module
from typing import Dict, List, Optional

from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse

logger = logging.getLogger(__name__)


class PluginManager:
    def __init__(self, app: FastAPI) -> None:
        self.app = app
        self.plugins = {}
        self.disabled_microservices = set()  # Track disabled microservices

    def register_microservice(
        self,
        microservice_name: str,
        config: Optional[Dict] = None,
        prefix: Optional[str] = None,
        tags: List[str] = None,
    ):
        """Register a microservice by its name, optional config, and route prefix"""
        try:
            module = import_module(f"microservices.{microservice_name}.routers")
            microservice_router = module.router

            # Use the provided prefix or default to the microservice name
            route_prefix = prefix or f"/{microservice_name}"
            route_tags = tags or [microservice_name]

            self.app.include_router(
                router=microservice_router, prefix=route_prefix, tags=route_tags
            )

            self.plugins[microservice_name] = {
                "router": microservice_router,
                "config": config or {},
                "prefix": route_prefix,
                "tags": route_tags,
            }

            logger.info(
                f"Microservice '{microservice_name}' registered successfully with prefix '{route_prefix}'"
            )
        except ModuleNotFoundError:
            logger.warning(f"Microservice '{microservice_name}' not found")
        except Exception as e:
            logger.error(f"Failed to register microservice '{microservice_name}': {e}")

    def initialise_microservices(self):
        """Initialize the registered microservices"""
        for microservice_name, plugin in self.plugins.items():
            if microservice_name in self.disabled_microservices:
                logger.info(
                    f"Microservice '{microservice_name}' is currently disabled and will not be initialized."
                )
                continue

            config = plugin["config"]
            if hasattr(plugin["router"], "initialise"):
                try:
                    plugin["router"].initialise(config)
                    logger.info(
                        f"Microservice '{microservice_name}' initialized with config: {config}"
                    )
                except Exception as e:
                    logger.error(
                        f"Failed to initialize microservice '{microservice_name}': {e}"
                    )

    def check_microservice_health(self, microservice_name: str) -> Optional[Dict]:
        """Check the health of a specific microservice"""
        if microservice_name in self.disabled_microservices:
            logger.info(
                f"Microservice '{microservice_name}' is currently disabled and its health cannot be checked."
            )
            return {
                "status": "disabled",
                "details": "Microservice is currently disabled",
            }

        try:
            module = import_module(f"microservices.{microservice_name}.health")
            health_check = module.check_health()
            return {"status": "healthy", "details": health_check}
        except ModuleNotFoundError:
            logger.warning(f"Health check module for '{microservice_name}' not found.")
            return {"status": "unhealthy", "details": "Health check module not found"}
        except Exception as e:
            logger.error(
                f"Failed to check health for microservice '{microservice_name}': {e}"
            )
            return {"status": "unhealthy", "details": str(e)}

    def disable_microservice(self, microservice_name: str):
        """Disable a microservice for maintenance"""
        if microservice_name not in self.plugins:
            logger.warning(
                f"Cannot disable microservice '{microservice_name}': not registered."
            )
            return

        self.disabled_microservices.add(microservice_name)
        logger.info(
            f"Microservice '{microservice_name}' has been disabled for maintenance."
        )

        # Add middleware to return a maintenance page for all routes of this microservice
        self.app.middleware("http")(self._maintenance_middleware(microservice_name))

    def enable_microservice(self, microservice_name: str):
        """Enable a microservice after maintenance"""
        if microservice_name not in self.disabled_microservices:
            logger.warning(
                f"Cannot enable microservice '{microservice_name}': not disabled."
            )
            return

        self.disabled_microservices.remove(microservice_name)
        logger.info(
            f"Microservice '{microservice_name}' has been enabled after maintenance."
        )

    def _maintenance_middleware(self, microservice_name: str):
        """Middleware to return a maintenance page for disabled microservice routes"""

        async def maintenance(request: Request, call_next):
            if request.url.path.startswith(self.plugins[microservice_name]["prefix"]):
                return HTMLResponse(
                    content="""
                        <h1>503 Service Unavailable</h1>
                        <p>This service is currently under maintenance. Please try again later.</p>
                        <p>Estimated Time of Availability: 12 OCT 2024 12:00 PM UTC</p>
                        <p>If you need immediate assistance, please contact support at <b>support@entweni.com</b></p>
                    """,
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                )
            return await call_next(request)

        return maintenance
