from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.drivers import router as drivers_router
from app.api.health import router as health_router
from app.api.orders import router as orders_router
from app.errors.handlers import register_exception_handlers


def create_app() -> FastAPI:
    app = FastAPI(title="Waypoint Partner Source API", version="1.0.0")
    register_exception_handlers(app)
    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(orders_router)
    app.include_router(drivers_router)
    return app


app = create_app()

