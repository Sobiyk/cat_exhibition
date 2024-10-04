from fastapi.routing import APIRouter

from .endpoints.breed import router as breed_router
from .endpoints.cat import router as cat_router

main_router = APIRouter(prefix='/api/v1')
main_router.include_router(breed_router)
main_router.include_router(cat_router)
