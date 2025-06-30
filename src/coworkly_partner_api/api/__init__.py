"""API routes for the CoWorkly Partner Dashboard API."""

from .spaces import router as spaces_router
from .posts import router as posts_router
from .features import router as features_router
from .health import router as health_router
from .dashboard_metrics import router as dashboard_metrics_router

__all__ = [
    "spaces_router",
    "posts_router", 
    "features_router",
    "health_router",
    "dashboard_metrics_router"
] 