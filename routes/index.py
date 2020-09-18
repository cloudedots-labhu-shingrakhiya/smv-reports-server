from fastapi import APIRouter
from .reports import router as reportsRouter

router = APIRouter()
router.include_router(reportsRouter)
