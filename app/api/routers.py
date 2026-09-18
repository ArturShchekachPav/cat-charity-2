from fastapi import APIRouter

from app.api.endpoints import charity_project, donation

main_router = APIRouter()
main_router.include_router(charity_project.router)
main_router.include_router(donation.router)
