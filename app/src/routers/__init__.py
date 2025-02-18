from .users_router import router as users_router
from .swagger import setup_swagger

__all__ = (
    "users_router",
    "setup_swagger",
)
