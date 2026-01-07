"""
API v1 router
"""
from fastapi import APIRouter

from app.api.v1 import calculators, auth, calculation_results, profiles, health, integrations

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, tags=["health"])
api_router.include_router(calculators.router, tags=["calculators"])
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(calculation_results.router, tags=["calculation_results"])
api_router.include_router(profiles.router, tags=["profiles"])
api_router.include_router(integrations.router, tags=["integrations"])
