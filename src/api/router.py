from fastapi import APIRouter
from .basket import router as basket_router

router = APIRouter()
router.include_router(basket_router)
