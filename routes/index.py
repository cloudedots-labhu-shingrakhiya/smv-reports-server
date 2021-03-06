from fastapi import APIRouter
# from .reports import router as reportsRouter
from routes.users.userReports import router as userRouter
from routes.sales.salesReports import router as salesRouter
from routes.customers.customers import router as customersRouter
from routes.upload import router as uploadRouter

router = APIRouter()
router.include_router(userRouter)
router.include_router(salesRouter)
router.include_router(customersRouter)
router.include_router(uploadRouter)
