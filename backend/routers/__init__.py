"""API routers for SteerMate backend."""

from routers.auth import router as auth_router
from routers.user import router as user_router
from routers.trips import router as trips_router
from routers.detection import router as detection_router

__all__ = ["auth_router", "user_router", "trips_router", "detection_router"]

