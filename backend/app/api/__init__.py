from fastapi import APIRouter
from app.api import auth, users, injuries, sports

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(injuries.router, prefix="/injuries", tags=["Injuries"])
api_router.include_router(sports.router, prefix="/sports", tags=["Sports"])
